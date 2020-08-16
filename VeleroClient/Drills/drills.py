from VeleroClient.velerohandler import *
from OpenShiftClient.openshifthandler import *
import time


def pre_checks():
    # Check for the Velero Operator in DR
    # Check to see if the Env's are present
    # Check the provided schedule is available
    # Check the status of work-loads
    pass


def fail_over(schedule: str) -> None:
    fo_restore_manifest = {
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
    # Begin FO
    logger.info(f"Performing Fail Over on Schedule : {schedule}")
    # Instantiate Velero Object
    fo = VeleroDRHandler()

    # Trigger Get Backups
    fo.get_backups(schedule=schedule)

    # Trigger Restoration
    for backup in fo.sort_backups:
        fo_restore_manifest['metadata']['name'] = f"ro-restored-{backup}"
        fo_restore_manifest.update({'spec': {"backupName": f"{backup}"}})
        try:
            sc, sr = fo.restore_scheduled_backups(restore_manifest=fo_restore_manifest)
            logger.info(f"RESTORE Successfully Triggerred ro-restored-{backup}, {sc, sr}")
            print(f"RO-Restored.... {backup}")
        except Exception as e:
            print(f"Failed restoring scheduled backups: {e}")
            return
    fo.restore_scheduled_backups(restore_manifest=fo_restore_manifest)

    # Work-Load Status Check
    podstat = (fo.recovered_pod_status())
    print(f"Protected Work-Loads:")
    for k, v in podstat['status'].items():
        if k == 'waiting':
            print(f" Pod Name: {podstat['name']} \n Pod Current Status: {k} \n Reason: {v['reason']} \n "
                  f"Message: {v['message']}")
        else:
            print(f"Pod Name: {podstat['name']}, \n Pod Current Status: {k}")


def failover_test_excercise(schedule: str) -> None:
    fote_restore_manifest = {
        "apiVersion": "velero.io/v1",
        "kind": "Restore",
        "metadata": {
            "name": "",
            "namespace": "velero"
        },
        "spec": {
            "backupName": "",
            "namespaceMapping": {
            }
        },
    }

    # Begin FOTE
    logger.info(f"Performing Fail Over Test Excercise on Schedule : {schedule}")
    fote = VeleroDRHandler()
    fote.get_backups(schedule=schedule)
    logger.info("Sorting Backups from backup list")
    for backup in fote.sort_backups:
        fote_restore_manifest['metadata']['name'] = f"ro-restored-{backup}"
        fote_restore_manifest.update({'spec': {"backupName": f"{backup}", 'namespaceMapping': {namespace:
                                               f"fote-{namespace}" for namespace in fote.protected_namespaces}}})
        try:
            sc, sr = fote.restore_scheduled_backups(restore_manifest=fote_restore_manifest)
            logger.info(f"RESTORE Successfully Triggerred ro-restored-{backup}, {sc, sr}")
            print(f"RO-Restored.... {backup}")
        except Exception as e:
            print(f"Failed restoring scheduled backups: {e}")
            return

    # Deployed Work-load Status Check
    for i in range(5):
        podstat = (fote.recovered_pod_status())
        print(f"Protected Work-Loads:")
        for k, v in podstat['status'].items():
            if k == 'waiting':
                print(f" Pod Name: {podstat['name']} \n Pod Current Status: {k} \n Reason: {v['reason']} \n "
                      f"Message: {v['message']}")
            else:
                print(f"Pod Name: {podstat['name']}, \n Pod Current Status: {k}")
        time.sleep(3)
        i += 1
    print("Work-Loads are Deployed in DR, please examine them,")

    # Prompt to delete Deployed Work-Loads
    workloads = True
    while workloads:
        workloaddelete = input("Once Done!!!, Please Enter 'delete' to delete all the created DR Work-Loads: ")
        if workloaddelete.lower() == 'delete':
            for namespace in fote.protected_namespaces:
                fote.delete_namespaces(namespaces=[f"fote-{namespace}"])
            workloads = False
            print("Deleted Scheduled Work-Loads in DR")
            logger.info("Deleted work-loads post FOTE in DR")


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
    return test.all_backups

# testget()

