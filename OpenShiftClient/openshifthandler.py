import enum
import requests
from DBDataEncrypter import dbdataencrypter
from presets import *


class Endpoints(str, enum.Enum):
    VELERO_GET_ALL = "/apis/velero.io/v1"
    VELERO_BACKUP = "/apis/velero.io/v1/namespaces/velero/backups/"
    VELERO_SCHEDULE = "/apis/velero.io/v1/namespaces/velero/schedule/"
    VELERO_RESTORE = "/apis/velero.io/v1/namespaces/velero/restores/"
    VELERO_STORAGE = "/apis/velero.io/v1/namespaces/velero/backupstoragelocations/"


class OpenshiftHandler:

    def __init__(self, secret) -> None:
        dbdata = dbdataencrypter.query_creds(dcrykey=secret)
        self.pr_url = dbdata[0]
        self.dr_url = dbdata[1]
        self.pr_token = dbdata[2]
        self.dr_token = dbdata[3]
        self.pr_token_header = {"Authorization": "Bearer " + self.pr_token}
        self.dr_token_header = {"Authorization": "Bearer " + self.dr_token}
        self.base_url = ""
        self.header = {}

    def get_pod_status(self, namespaces: list) -> dict or None:
        container_status = {}
        for namespace in namespaces:
            podstatus = f"/api/v1/namespaces/{namespace}/pods"
            try:
                response = requests.get(self.base_url + podstatus, headers=self.header, verify=False, timeout=10)
                if not response.ok:
                    logger.error(f"ERROR Unable to get Pod Status: {response.status_code}, {response.reason}")
                    return None
                logger.info(f"GET Pod status successfully retrieved: {response.status_code}")
                for pod in response.json()['items']:
                    try:
                        for status in pod['status']['containerStatuses']:
                            for k, v in status['state'].items():
                                container_status.update({"name": status['name'], "status": {k: v}})
                    except KeyError:
                        pass
            except Exception as e:
                print("Error Occurred while getting Pod Status: ", e)
                logger.debug(f"Error Occurred while getting Pod Status: , {e}")
                return None
        return container_status

    def delete_namespaces(self, namespaces: list) -> dict or None:
        for ns in namespaces:
            namespace = f"/api/v1/namespaces/{ns}"
            try:
                logger.info(f"Delete Triggerred Successfully, Deleting Namespace: {ns}")
                response = requests.delete(self.base_url + namespace, headers=self.header, verify=False, timeout=10)
                if not response.ok:
                    logger.error(f"ERROR Unable to delete Namespace: {response.status_code}, {response.reason}")
                    return None
            except Exception as e:
                print(f"Error Occurred while deleting Namespaces: {ns}, {e}")
                logger.debug(f"Error Occurred while deleting Namespaces: {ns} , {e}")
                return None

class OpenshiftPRHandler(OpenshiftHandler):
    def __init__(self, secret):
        super().__init__(secret=secret)
        self.base_url = self.pr_url
        self.header = self.pr_token_header


class OpenshiftDRHandler(OpenshiftHandler):
    def __init__(self, secret):
        super().__init__(secret=secret)
        self.base_url = self.dr_url
        self.header = self.dr_token_header
