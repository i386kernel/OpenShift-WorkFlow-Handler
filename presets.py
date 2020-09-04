import logging
import urllib3
import sys


# Data Path for DB and Log Files
DATA_PATH = r"/var/lib/opworkflowmanager/"
# DATA_PATH = ""

# Logger Config
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
try:
    file_handler = logging.FileHandler(DATA_PATH+"opworkflow.log")
except Exception as loge:
    print(f"Error Unable to Create Log file in the specified location : {loge}")
    sys.exit(1)
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# urllib3 Disable Warnings
urllib3.disable_warnings()
