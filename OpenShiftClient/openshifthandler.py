import enum
import logging
import requests
import urllib3

# Presets for Logging and urllib3 disable warnings
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)
# logger.setLevel(logging.CRITICAL)
# logger.setLevel(logging.ERROR)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler = logging.FileHandler("test.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Disable cert warnings
urllib3.disable_warnings()

# Initialize Enums
class Endpoints(str, enum.Enum):
    VELERO_BACKUP = "/apis/velero.io/v1/namespaces/velero/backups/"
    VELERO_SCHEDULE = "/apis/velero.io/v1/namespaces/velero/schedule/"
    VELERO_RESTORE = "/apis/velero.io/v1/namespaces/velero/restores/"
    VELERO_STORAGE = "/apis/velero.io/v1/namespaces/velero/backupstoragelocations/"

# Check this Diff

class OpenShiftHandler:

    # def __init__(self) -> None:
    #     self.pr_url = os.getenv("PR_URL")
    #     self.dr_url = os.getenv("DR_URL")
    #     self.pr_token = os.getenv("PR_TOKEN")
    #     self.dr_token = os.getenv("DR_TOKEN")
    #     self.pr_token_header = {"Authorization": "Bearer " + self.pr_token}
    #     self.dr_token_header = {"Authorization": "Bearer " + self.dr_token}
    #     def set_pr_token_header(self) -> dict:
    #       return {'Authorization': 'Bearer ' + self.pr_token}
    #     def set_dr_token_header(self) -> dict:
    #       return {'Authorization': 'Bearer ' + self.dr_token}

    def __init__(self) -> None:
        self.pr_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNTYmFBWDRtRklVZmVxMzhFUXZNV1BsTmw2RXNHZ0wwQUR2TGJWTkNtME0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJjbHVzdGVyYWRtaW4tdG9rZW4tbnhwNW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiY2x1c3RlcmFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZDQxYjkwZjctNDMwMS00YTE5LWIxMTItZjRhNTFmMGNhZGI3Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmNsdXN0ZXJhZG1pbiJ9.bZPZ10Vt_qsXoA2Ai1RImmyULiGP5UTHFCAYcqeixv6md0G90kwMyTe68VyrdTJT9Ks2urslU88U0vVhWrB2vYTZBF68Sip5uLe3f_yVjAFXdfeFwY2lFj8_tCi0CxWmOW9cZJ7r5E9gaTTVUij-CXobxCWsaukNvNZU9u4Hss6FPaLrq0addoVBPjO1QR_SspcV0ZtSm_1-VXKR0vn4cdrf-_Ifhswu1uB2iWDdpfjRZTCh6w0bUkphfQaqQwGI9tKHWhUuOe7D8h9j9aEzQoDQxoVYwHhOvv2pdJfPTcm3cydr0Rxtv3VrcMkHg7jk0QrhZtGaIsUwJaxWqApKUQ"
        self.dr_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJjbHVzdGVyYWRtaW4tdG9rZW4tbjI2Y2oiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiY2x1c3RlcmFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiMTdhZDg4ODgtZDMwNC0xMWVhLThlODktMDA1MDU2YWQwMDgzIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmNsdXN0ZXJhZG1pbiJ9.DlXFhuBQncBqFnIccYQ_6B2mHGnngarbNhTS5-7o90gtC8awTzRcgy9Dze_3pBAHgeFI0qQnliI-5pS7Q5gCzGcONfxvDOqTiJ1ehV-cyMvkbK8n-2EEUkkIjTGKBoZ7_FdjH7JzuaouwGCcyF0XU2w_OJxzqEl8mXLFQK8SOyWlVLy3ZohWxkmKjcKAafF-lGzW-l0PX9vykL975xGeRX3FcB9BOXkn5hgCFmWS7q7OuVnrwXQUFLGsrLIT1ngSf5QTFKsbpllPwd4RosFtpHqYmEqh1Zd4hqr9np5pceZp4xjMuBaiwRzkjj7vFlwngi2Kn43rrl_sWht7kHF6vg"
        self.pr_url = "https://192.168.8.129:6443"
        self.dr_url = "https://192.168.8.53:6443"
        self.pr_token_header = {"Authorization": "Bearer " + self.pr_token}
        self.dr_token_header = {"Authorization": "Bearer " + self.dr_token}

    def get_pod_status(self, baseurl: str, headers: dict, namespaces: list) -> None:

        for namespace in namespaces:
            podstatus = f"/api/v1/namespaces/{namespace}/pods/"
            response = requests.get(baseurl + podstatus, headers=headers, verify=False, timeout=10)
            return response.json()

