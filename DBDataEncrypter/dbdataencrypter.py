import sqlite3
from base64 import b64encode, b64decode
from sqlite3 import Error
from presets import *
from cryptography.fernet import Fernet
import cryptography

secretkey = Fernet.generate_key()


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
                return c.fetchall()
            except Error as e:
                print(e)

    @staticmethod
    def db_data_encode(encodingstr: str):
        # Encode string to byte string
        bstring = encodingstr.encode('utf-8')

        # Encode bytes to base64 byte string and decode it to utf-8
        return b64encode(bstring).decode('utf-8')

    @staticmethod
    def db_data_decode(decodingstr: str):
        # Encode decoding string to byte string
        bstring = decodingstr.encode('utf-8')

        # Decode bytes to base64 byte string and decode it to utf-8
        return b64decode(bstring).decode('utf-8')

    @staticmethod
    def db_data_encrypt(encryptstr: str):
        f = Fernet(secretkey)
        return f.encrypt(encryptstr.encode()).decode()

    @staticmethod
    def db_data_decrypt(decryptstr: str, dcrykey: str):
        f = Fernet(dcrykey.encode())
        try:
            return f.decrypt(decryptstr.encode()).decode()
        except cryptography.fernet.InvalidToken as e:
            print(f"Invalid Token, unable to decrypt, please makes sure to insert Valid Token....Exiting...: {e}")
            sys.exit(1)


def insert_cred_data(pr_url: str, dr_url: str, pr_token: str, dr_token: str):
    cred_table = """CREATE TABLE IF NOT EXISTS opworkflowtable (
                        pr_url blob NOT NULL,
                        dr_url blob NOT NULL,
                        pr_token blob NOT NULL,
                        dr_token blob NOT NULL
                        ); """
    try:
        sqlobj = SqlDataEncode(DATA_PATH+"opworkflowmanager.db")
        sqlobj.execute_query(cred_table)
        logger.info("Adding Encrypted Creds to DB")
        sqlobj.execute_query(f"INSERT INTO opworkflowtable VALUES ('{sqlobj.db_data_encrypt(pr_url)}', "
                             f"'{sqlobj.db_data_encrypt(dr_url)}', '{sqlobj.db_data_encrypt(pr_token)}', "
                             f"'{sqlobj.db_data_encrypt(dr_token)}')")
        logger.info(f"Successfylly able to add creds data into db")
        print(f"Data Encrypted in DB, Save this key to decrypt it in future: {secretkey.decode()}")
    except Exception as e:
        logger.critical(f"Unable to Insert data into DB: {e}")
        sys.exit(1)


def query_creds(dcrykey: str) -> list:
    try:
        sqlobj = SqlDataEncode(DATA_PATH+'opworkflowmanager.db')
        row = sqlobj.execute_query("SELECT * from opworkflowtable")
        logger.info(f"Successfylly able to retrieve creds data from db")
        return [sqlobj.db_data_decrypt(decryptstr=item, dcrykey=dcrykey) for item in row[-1]]

    except Exception as e:
        print(f"Unable to retrieve data from DB, make sure the token is valid, exiting...: {e}")
        logger.critical(f"Unable to retrieve data from DB, make sure the token is valid, exiting...: {e}")
        sys.exit(1)
