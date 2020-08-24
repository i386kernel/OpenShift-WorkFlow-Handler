import enum
import requests
from DBDataEncoder import dbdataencoder
from presets import *


class Endpoints(str, enum.Enum):
    VELERO_GET_ALL = "/apis/velero.io/v1"
    VELERO_BACKUP = "/apis/velero.io/v1/namespaces/velero/backups/"
    VELERO_SCHEDULE = "/apis/velero.io/v1/namespaces/velero/schedule/"
    VELERO_RESTORE = "/apis/velero.io/v1/namespaces/velero/restores/"
    VELERO_STORAGE = "/apis/velero.io/v1/namespaces/velero/backupstoragelocations/"


class OpenshiftHandler:

    # def __init__(self) -> None:
    #     self.pr_url = os.getenv("PR_URL")
    #     self.dr_url = os.getenv("DR_URL")
    #     self.pr_token = os.getenv("PR_TOKEN")
    #     self.dr_token = os.getenv("DR_TOKEN")
    #     self.pr_token_header = {"Authorization": "Bearer " + self.pr_token}
    #     self.dr_token_header = {"Authorization": "Bearer " + self.dr_token}
    #     self.base_url = ""
    #     self.header = {}

    # def __init__(self) -> None:
    #     self.pr_token = """eyJhbGciOiJSUzI1NiIsImtpZCI6ImNTYmFBWDRtRklVZmVxMzhFUXZNV1BsTmw2RXNHZ0wwQUR2TGJWTkNtME0ifQ.
    #     eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlL
    #     XN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJjbHVzdGVyYWRtaW4tdG9rZW4tbnhwNW4iLCJrdW
    #     Jlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiY2x1c3RlcmFkbWluIiwia3ViZXJuZXRlcy5pby9zZX
    #     J2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZDQxYjkwZjctNDMwMS00YTE5LWIxMTItZjRhNTFmMGNhZGI3Iiwic3ViIjoic3
    #     lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmNsdXN0ZXJhZG1pbiJ9.bZPZ10Vt_qsXoA2Ai1RImmyULiGP5UTHFCAYcqeixv6md0
    #     G90kwMyTe68VyrdTJT9Ks2urslU88U0vVhWrB2vYTZBF68Sip5uLe3f_yVjAFXdfeFwY2lFj8_tCi0CxWmOW9cZJ7r5E9gaTTVUij-CXobxCW
    #     saukNvNZU9u4Hss6FPaLrq0addoVBPjO1QR_SspcV0ZtSm_1-VXKR0vn4cdrf-_Ifhswu1uB2iWDdpfjRZTCh6w0bUkphfQaqQwGI9tKHWhUu
    #     Oe7D8h9j9aEzQoDQxoVYwHhOvv2pdJfPTcm3cydr0Rxtv3VrcMkHg7jk0QrhZtGaIsUwJaxWqApKUQ"""
    #     self.dr_token = """eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2Nv
    #     dW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2Vydm
    #     ljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJjbHVzdGVyYWRtaW4tdG9rZW4tbjI2Y2oiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uY
    #     W1lIjoiY2x1c3RlcmFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiMTdhZDg4ODgtZDM
    #     wNC0xMWVhLThlODktMDA1MDU2YWQwMDgzIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmNsdXN0ZXJhZG1pbiJ9
    #     .DlXFhuBQncBqFnIccYQ_6B2mHGnngarbNhTS5-7o90gtC8awTzRcgy9Dze_3pBAHgeFI0qQnliI-5pS7Q5gCzGcONfxvDOqTiJ1ehV-cyMvkb
    #     K8n-2EEUkkIjTGKBoZ7_FdjH7JzuaouwGCcyF0XU2w_OJxzqEl8mXLFQK8SOyWlVLy3ZohWxkmKjcKAafF-lGzW-l0PX9vykL975xGeRX3Fc
    #     B9BOXkn5hgCFmWS7q7OuVnrwXQUFLGsrLIT1ngSf5QTFKsbpllPwd4RosFtpHqYmEqh1Zd4hqr9np5pceZp4xjMuBaiwRzkjj7vFlwngi2Kn
    #     43rrl_sWht7kHF6vg"""
    #     self.pr_url = "https://192.168.8.129:6443"
    #     self.dr_url = "https://192.168.8.53:6443"
    #     self.pr_token_header = {"Authorization": "Bearer " + self.pr_token}
    #     self.dr_token_header = {"Authorization": "Bearer " + self.dr_token}
    #     self.base_url = ""
    #     self.header = {}

    def __init__(self) -> None:
        dbdata = dbdataencoder.query_creds()
        self.pr_url = dbdata[0]
        self.dr_url = dbdata[1]
        self.pr_token = dbdata[2]
        self.dr_token = dbdata[3]
        self.pr_token_header = {"Authorization": "Bearer " + self.pr_token}
        self.dr_token_header = {"Authorization": "Bearer " + self.dr_token}
        self.base_url = ""
        self.header = {}

    def get_pod_status(self, namespaces: list,  namespaceprefix: str = "", ) -> dict or None:
        container_status = {}
        for namespace in namespaces:
            podstatus = f"/api/v1/namespaces/{namespaceprefix}{namespace}/pods"
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
    def __init__(self):
        super().__init__()
        self.base_url = self.pr_url
        self.header = self.pr_token_header


class OpenshiftDRHandler(OpenshiftHandler):
    def __init__(self):
        super().__init__()
        self.base_url = self.dr_url
        self.header = self.dr_token_header
