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
            response = requests.get(self.base_url + Endpoints.VELERO_BACKUP, headers=self.header, verify=False, timeout=10)
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
    def sort_backups(self) -> list:
        """Sorts the Backups
       :arg
        None
       :returns
        None
       """
        drbackuplist = self.all_backups.copy()
        drbackuplist.sort(key=lambda sort_backup: sort_backup.split("-")[-1])
        return drbackuplist

    def restore_scheduled_backups(self, restore_obj: dict) -> None:
        """Restores sorted backups
         :arg
            baseurl => Openshift Base URL, headers => http Headers, restoreobj => Post Body
         :returns
            None
        """
        if not self.sort_backups:
            print("There are no scheduled backups available!!!")
            return
        logger.info("Sorting Backups from backup list")
        for backup in self.sort_backups:
            restore_obj['metadata']['name'] = f"ro-restored-{backup}"
            restore_obj['spec']['backupName'] = backup
            try:
                response = requests.post(self.base_url + Endpoints.VELERO_RESTORE, headers=self.header,
                                         verify=False, json=restore_obj, timeout=10)
                if not response.ok:
                    logger.critical(f"ERROR Unable to Restore Backups: {response.status_code}, {response.reason}")
                    print(f"ERROR...Unable to Restore Backups: {response.status_code}, {response.reason}")
                    return
                logger.info(f"RESTORE Successfully Triggerred ro-restored-{backup}, {response.status_code}")
                print(f"RO-Restored.... {backup}")
            except Exception as e:
                print("Error While restoring Backups: ", e)
                logger.debug(f"Error Occourred while restoring backups: {e}")
                sys.exit(1)
        return None

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
            baseurl => Openshift Base URL, headers => http Headers
          :returns
            Dict or None
        """
        try:
            response = requests.get(self.base_url + Endpoints.VELERO_STORAGE, headers=self.header, verify=False, timeout=10)
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

    def recovered_pod_status(self) -> dict:
        """Gets status of recovered Pods
            :arg
              baseurl => Openshift Base URL, headers => http Headers
            :returns
              None
        """
        return self.get_pod_status(namespaces=self.protected_namespaces)


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

