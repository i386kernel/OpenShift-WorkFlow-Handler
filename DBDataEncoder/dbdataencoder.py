import sqlite3
import base64
from sqlite3 import Error
from OpenShiftClient.openshifthandler import *
import sys

# pr_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6ImNTYmFBWDRtRklVZmVxMzhFUXZNV1BsTmw2RXNHZ0wwQUR2TGJWTkNtME0ifQ.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJjbHVzdGVyYWRtaW4tdG9rZW4tbnhwNW4iLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiY2x1c3RlcmFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiZDQxYjkwZjctNDMwMS00YTE5LWIxMTItZjRhNTFmMGNhZGI3Iiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmNsdXN0ZXJhZG1pbiJ9.bZPZ10Vt_qsXoA2Ai1RImmyULiGP5UTHFCAYcqeixv6md0G90kwMyTe68VyrdTJT9Ks2urslU88U0vVhWrB2vYTZBF68Sip5uLe3f_yVjAFXdfeFwY2lFj8_tCi0CxWmOW9cZJ7r5E9gaTTVUij-CXobxCWsaukNvNZU9u4Hss6FPaLrq0addoVBPjO1QR_SspcV0ZtSm_1-VXKR0vn4cdrf-_Ifhswu1uB2iWDdpfjRZTCh6w0bUkphfQaqQwGI9tKHWhUuOe7D8h9j9aEzQoDQxoVYwHhOvv2pdJfPTcm3cydr0Rxtv3VrcMkHg7jk0QrhZtGaIsUwJaxWqApKUQ"
# dr_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IiJ9.eyJpc3MiOiJrdWJlcm5ldGVzL3NlcnZpY2VhY2NvdW50Iiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9uYW1lc3BhY2UiOiJrdWJlLXN5c3RlbSIsImt1YmVybmV0ZXMuaW8vc2VydmljZWFjY291bnQvc2VjcmV0Lm5hbWUiOiJjbHVzdGVyYWRtaW4tdG9rZW4tbjI2Y2oiLCJrdWJlcm5ldGVzLmlvL3NlcnZpY2VhY2NvdW50L3NlcnZpY2UtYWNjb3VudC5uYW1lIjoiY2x1c3RlcmFkbWluIiwia3ViZXJuZXRlcy5pby9zZXJ2aWNlYWNjb3VudC9zZXJ2aWNlLWFjY291bnQudWlkIjoiMTdhZDg4ODgtZDMwNC0xMWVhLThlODktMDA1MDU2YWQwMDgzIiwic3ViIjoic3lzdGVtOnNlcnZpY2VhY2NvdW50Omt1YmUtc3lzdGVtOmNsdXN0ZXJhZG1pbiJ9.DlXFhuBQncBqFnIccYQ_6B2mHGnngarbNhTS5-7o90gtC8awTzRcgy9Dze_3pBAHgeFI0qQnliI-5pS7Q5gCzGcONfxvDOqTiJ1ehV-cyMvkbK8n-2EEUkkIjTGKBoZ7_FdjH7JzuaouwGCcyF0XU2w_OJxzqEl8mXLFQK8SOyWlVLy3ZohWxkmKjcKAafF-lGzW-l0PX9vykL975xGeRX3FcB9BOXkn5hgCFmWS7q7OuVnrwXQUFLGsrLIT1ngSf5QTFKsbpllPwd4RosFtpHqYmEqh1Zd4hqr9np5pceZp4xjMuBaiwRzkjj7vFlwngi2Kn43rrl_sWht7kHF6vg"
# pr_url = "https://192.168.8.129:6443"
# dr_url = "https://192.168.8.53:6443"


class SqlDataEncode:
    def __init__(self, db_file):
        self.db_file = db_file

    def create_connection(self):
        """Create a DB Connection to sqlite3"""
        try:
            conn = sqlite3.connect(self.db_file)
            return conn
        except Error as e:
            print(e)

    def execute_query(self, query: str):
        conn = self.create_connection()
        if self.create_connection() is not None:
            try:
                c = conn.cursor()
                c.execute(query)
                conn.commit()
                return c.fetchone()
            except Error as e:
                print(e)

    @staticmethod
    def db_data_encode(encodingstr: str):
        # Encode string to byte string
        bstring = encodingstr.encode('utf-8')

        # Encode bytes to base64 byte string and decode it to utf-8
        return base64.b64encode(bstring).decode('utf-8')

    @staticmethod
    def db_data_decode(decodingstr: str):
        # Encode decoding string to byte string
        bstring = decodingstr.encode('utf-8')

        # Decode bytes to base64 byte string and decode it to utf-8
        return base64.b64decode(bstring).decode('utf-8')


def insert_cred_data(pr_url: str, dr_url: str, pr_token: str, dr_token: str):
    cred_table = """CREATE TABLE IF NOT EXISTS opworkflowtable (
                        pr_url blob NOT NULL,
                        dr_url blob NOT NULL,
                        pr_token blob NOT NULL,
                        dr_token blob NOT NULL
                        ); """
    try:
        sqlobj = SqlDataEncode("opworkflowmanager.db")
        sqlobj.execute_query(cred_table)
        sqlobj.execute_query(f"INSERT INTO opworkflowtable VALUES ('{sqlobj.db_data_encode(pr_url)}', "
                             f"'{sqlobj.db_data_encode(dr_url)}', '{sqlobj.db_data_encode(pr_token)}', "
                             f"'{sqlobj.db_data_encode(dr_token)}')")
        logger.info(f"Successfylly able to add creds data into db")
    except Exception as e:
        logger.critical(f"Unable to Insert data into DB: {e}")
        sys.exit(1)


def query_creds() -> list:
    decoded_dbdata = []
    try:
        sqlobj = SqlDataEncode('opworkflowmanager.db')
        row = sqlobj.execute_query("SELECT * from opworkflowtable")
        for item in row:
            decoded_dbdata.append(sqlobj.db_data_decode(item))
        return decoded_dbdata
    except Exception as e:
        logger.critical(f"Unable to retrieve data from DB: {e}")
        sys.exit(1)
