import sys
from OpenShiftClient.openshifthandler import *


class VeleroHandler(OpenshiftHandler):
    def __init__(self) -> None:
        super().__init__()
        self.all_backups = []
        self.protected_namespaces = []

    def get_backups(self, schedule: str) -> None:
        """Gets all scheduled backups
       :arg
        baseurl => Openshift Base URL, headers => http Headers
       :returns
        None
       """
        try:
            response = requests.get(self.base_url + Endpoints.VELERO_BACKUP, headers=self.header, verify=False,
                                    timeout=10)
            if not response.ok:
                logger.critical(f"ERROR Unable to Retrieve Backups: {response.status_code}, {response.reason}")
                return
            logger.info(f"GET Backups Successfully Triggerred - Status Code: {response.status_code}")
            for backup in response.json()['items']:
                try:
                    if (backup['metadata']['labels']['velero.io/schedule-name'] == schedule) and (
                            backup['status']['phase']) == 'Completed':
                        self.all_backups.append(backup['metadata']['name'])
                        if not self.protected_namespaces:
                            self.protected_namespaces = backup['spec']['includedNamespaces'].copy()
                except KeyError:
                    pass
        except Exception as e:
            print("Error Occourred during getting Backups: ", e)
            logger.debug(f"Error Occourred during Retrieving Backups: , {e}")
            sys.exit(1)
        return None

    @property
    def sort_backups(self) -> list or None:
        """Sorts the Backups
       :arg
        None
       :returns
        None
       """
        drbackuplist = self.all_backups.copy()
        drbackuplist.sort(key=lambda sort_backup: sort_backup.split("-")[-1])
        if not drbackuplist:
            raise LookupError("Unable to find the given Schedule")
        return drbackuplist

    def restore_scheduled_backups(self, restore_manifest: dict) -> (int, str) or None:
        """Restores sorted backups
         :arg
            baseurl => Openshift Base URL, headers => http Headers, restoreobj => Post Body
         :returns
            None
        """
        if not self.sort_backups:
            print("There are no scheduled backups available!!!")
            return
        try:
            response = requests.post(self.base_url + Endpoints.VELERO_RESTORE, headers=self.header,
                                     verify=False, json=restore_manifest, timeout=10)
            if not response.ok:
                logger.critical(f"ERROR Unable to Restore Backups: {response.status_code}, {response.reason}")
                print(f"ERROR...Unable to Restore Backups: {response.status_code}, {response.reason}")
                return
            return response.status_code, response.reason
        except Exception as e:
            print("Error While restoring Backups: ", e)
            logger.debug(f"Error Occourred while restoring backups: {e}")
            sys.exit(1)

    def get_restores(self) -> dict or None:
        """Gets performed restores
          :arg
            baseurl => Openshift Base URL, headers => http Headers
          :returns
            None
        """
        response = requests.get(self.base_url + Endpoints.VELERO_RESTORE, headers=self.header, verify=False, timeout=10)
        if not response.ok:
            logger.critical(f"ERROR Unable to Get Restores: {response.status_code}, {response.reason}")
            return
        logger.info(f"RESTORES, {response.status_code}")
        return response.json()

    def get_storage_location(self) -> dict or None:
        """Gets storage locations
          :arg
            baseurl -> Openshift Base URL, headers -> http Headers
          :returns
            Dict or None
        """
        try:
            response = requests.get(self.base_url + Endpoints.VELERO_STORAGE, headers=self.header, verify=False,
                                    timeout=10)
            if not response.ok:
                logger.critical(f"ERROR Unable to Retrieve Storage Location: {response.status_code}, {response.reason}")
                return
            logger.info(f"{response.status_code}, {response.reason} Storage Location GET Triggerred")
            return response.json()
        except Exception as e:
            print(f"Error occoured while getting storage location: {e}")

    def change_storage_access(self):
        """Gets performed restores
          :arg
            baseurl => Openshift Base URL, headers => http Headers
          :returns
            None
        """
        try:
            response = requests.post(self.base_url + Endpoints.VELERO_STORAGE, headers=self.header, verify=False,
                                     timeout=10)
            if not response.ok:
                logger.critical(f"ERROR Unable to Retrieve Storage Location: {response.status_code}, {response.reason}")
                return
            logger.info(f"{response.status_code}, {response.reason} Storage Location GET Triggerred")
            return response.json()
        except Exception as e:
            print(f"Error occoured while changing the storage location: {e}")

    def recovered_pod_status(self, namespaceprefix: str = "") -> dict:
        """Gets status of recovered Pods"""
        return self.get_pod_status(namespaces=self.protected_namespaces, namespaceprefix=namespaceprefix)

    def velero_conn_check(self) -> bool:
        """Checks if it can reach Velero Instance"""
        try:
            response = requests.get(self.base_url + Endpoints.VELERO_GET_ALL, headers=self.header, verify=False,
                                    timeout=10)
            if not response.ok:
                print(f"Unable to Communicate or Authenticate with {self.base_url}{Endpoints.VELERO_GET_ALL}, "
                      f"{response.status_code}")
                logger.debug(f"Error Unable to communicate or Authenticate with {self.base_url}"
                             f"{Endpoints.VELERO_GET_ALL}"
                             f"{response.status_code}")
                return False
            print(f"Successfully able to connect and authenticate with {self.base_url}{Endpoints.VELERO_GET_ALL}, "
                  f"{response.status_code}")
            logger.info(f"Successfully able to authenticate with {self.base_url}{Endpoints.VELERO_GET_ALL}"
                        f"{response.status_code}")
            return True
        except Exception as e:
            print(f"Error occured while trying to communicate with {self.base_url}")
            logger.debug(f"Error occured while trying to communicate with {self.base_url}: {e}")


class VeleroPRHandler(VeleroHandler):
    def __init__(self):
        super().__init__()
        self.base_url = self.pr_url
        self.header = self.pr_token_header


class VeleroDRHandler(VeleroHandler):
    def __init__(self):
        super().__init__()
        self.base_url = self.dr_url
        self.header = self.dr_token_header
