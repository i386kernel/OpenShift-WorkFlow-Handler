from VeleroClient.velerohandler import *
from OpenShiftClient.openshifthandler import *


def pre_checks():
    # Check for the Velero Operator in DR

    # Check to see if the Env's are present
    # Check the provided schedule is available
    # Check the status of work-loads
    pass


def fail_over(schedule: str) -> None:
    fo_restore_obj = {
        "apiVersion": "velero.io/v1",
        "kind": "Restore",
        "metadata": {
            "name": "",
            "namespace": "velero"
        },
        "spec": {
            "backupName": ""
        }
    }
    logger.info(f"Performing Fail Over on Schedule : {schedule}")
    fo = VeleroDRHandler()
    fo.get_backups(schedule=schedule)
    fo.restore_scheduled_backups(restore_obj=fo_restore_obj)


def failover_test_excercise(schedule: str) -> None:
    fote_restore_obj = {
        "apiVersion": "velero.io/v1",
        "kind": "Restore",
        "metadata": {
            "name": "",
            "namespace": "velero"
        },
        "spec": {
            "backupName": ""
        }
    }
    logger.info(f"Performing Fail Over Test Excercise on Schedule : {schedule}")
    fote = VeleroDRHandler()
    fote.get_backups(schedule=schedule)
    fote.restore_scheduled_backups(restore_obj=fote_restore_obj)
    podstat = (fote.recovered_pod_status())
    for k, v in podstat['status'].items():
        if k == 'waiting':
            print(f"Pod Name: {podstat['name']}, \n Pod Current Status: {k} \n Reason: {v['reason']} \n "
                  f"Message: {v['message']}")
        else:
            print(f"Pod Name: {podstat['name']}, \n Pod Current Status: {k}")


def fall_back():
    print("Not Available")
    pass


def switch_over() -> None:
    backup_location_object = {
        "apiVersion": "velero.io/v1",
        "kind": "BackupStorageLocation",
        "metadata": {
            "name": "default",
            "namespace": "velero",
        },
        "spec": {
            "accessMode": "ReadOnly",
            "objectStorage": {
                "bucket": "velero"
            },
            "provider": "aws"
        }
    }
    print("Not Available")
    pass


def switch_back():
    print("Not Available")
    pass


def testget():
    test = VeleroDRHandler()
    test.get_backups(schedule="sched-backup-01")
    print(test.all_backups)

# testget()

#
# def testget():
#     test = VeleroHandler()
#     test.get_backups(test.dr_url, test.dr_token_header)
#     print(test.getallbackups)
#     test.sort_backups()
#     print(f"Sorted Backups: {test.sortedbackups}")
#     print(test.get_restores(test.dr_url, test.dr_token_header))
#     print(test.get_storage_location(test.dr_url, test.dr_token_header))
#
# testget()
#
