import sys
from OpenShiftClient.openshifthandler import *


class VeleroHandler(OpenShiftHandler):
    def __init__(self) -> None:
        super().__init__()
        self.all_backups = []
        # self.sorted_backups = []

    def get_backups(self, baseurl: str, headers: dict, schedule: str) -> None:
        """Gets all scheduled backups
       :arg
        baseurl => Openshift Base URL, headers => http Headers
       :returns
        None
       """
        try:
            response = requests.get(baseurl + Endpoints.VELERO_BACKUP, headers=headers, verify=False, timeout=10)
            if not response.ok:
                logger.critical(f"ERROR Unable to Retrieve Backups: {response.status_code}, {response.reason}")
                return
            logger.info(f"GET Backups Successfully Triggerred - Status Code: {response.status_code}, Retrieved - "
                        f" {len(response.json()['items'])} backups")
            for backup in response.json()['items']:
                try:
                    if (backup['metadata']['labels']['velero.io/schedule-name'] == schedule) and (
                            backup['status']['phase']) == 'Completed':
                        self.all_backups.append(backup['metadata']['name'])
                except KeyError:
                    pass
        except Exception as e:
            print("Error Occourred during getting Backups: ", e)
            logger.error(f"Error Occourred during Retrieving Backups: , {e}")
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
        logger.info("Sorting Backups from backup list")
        drbackuplist.sort(key=lambda x: x.split("-")[-1])
        return drbackuplist

    def restore_scheduled_backups(self, baseurl: str, headers: dict, restore_obj: dict) -> dict or None:
        """Restores sorted backups
         :arg
            baseurl => Openshift Base URL, headers => http Headers, restoreobj => Post Body
         :returns
            None
        """

        if not self.sort_backups:
            print("There are no scheduled backups available!!!")
            return
        for backup in self.sort_backups:
            restore_obj['metadata']['name'] = f"ro-restored-{backup}"
            restore_obj['spec']['backupName'] = backup
            try:
                response = requests.post(baseurl + Endpoints.VELERO_RESTORE, headers=headers,
                                         verify=False, json=restore_obj, timeout=10)
                if not response.ok:
                    logger.critical(f"ERROR Unable to Restore Backups: {response.status_code}, {response.reason}")
                    print(f"ERROR...Unable to Restore Backups: {response.status_code}, {response.reason}")
                    return
                logger.info(f"RESTORE Successfully Triggerred ro-restored-{backup}, {response.status_code}")
                print(f"RO-Restored.... {backup}")
            except Exception as e:
                print("Error While restoring Backups: ", e)
                logger.error(f"Error Occourred while restoring backups: , {e}")
                sys.exit(1)
        return None

    @staticmethod
    def get_restores(baseurl: str, headers: dict) -> dict or None:
        """Gets performed restores
          :arg
            baseurl => Openshift Base URL, headers => http Headers
          :returns
            None
        """
        response = requests.get(baseurl + Endpoints.VELERO_RESTORE, headers=headers, verify=False, timeout=10)
        if not response.ok:
            logger.critical(f"ERROR Unable to Get Restores: {response.status_code}, {response.reason}")
            return
        logger.info(f"RESTORES, {response.status_code}")
        return response.json()

    @staticmethod
    def get_storage_location(baseurl: str, headers: dict) -> dict or None:
        """Gets storage locations
          :arg
            baseurl => Openshift Base URL, headers => http Headers
          :returns
            Dict or None
        """
        try:
            response = requests.get(baseurl + Endpoints.VELERO_STORAGE, headers=headers, verify=False, timeout=10)
            if not response.ok:
                logger.critical(f"ERROR Unable to Retrieve Storage Location: {response.status_code}, {response.reason}")
                return
            logger.info(f"{response.status_code}, {response.reason} Storage Location GET Triggerred")
            return response.json()
        except Exception as e:
            print(f"Error occoured while getting storage location: {e}")

    def change_storage_mode(self):
        """Gets performed restores
          :arg
            baseurl => Openshift Base URL, headers => http Headers
          :returns
            None
        """
        pass

    def get_velero_recovered_pod_status(self, baseurl: str, headers: str) -> dict:
        """Gets status of recovered Pods
            :arg
              baseurl => Openshift Base URL, headers => http Headers
            :returns
              None
        """

