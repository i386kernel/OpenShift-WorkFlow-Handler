from VeleroClient.velerohandler import VeleroHandler


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

    fo = VeleroHandler()
    fo.get_backups(fo.dr_url, fo.dr_token_header, schedule)
    print(fo.restore_scheduled_backups(baseurl=fo.dr_url, headers=fo.dr_token_header, restore_obj=fo_restore_obj))


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

    fote = VeleroHandler()
    fote.get_backups(fote.dr_url, fote.dr_token_header, schedule)
    fote.restore_scheduled_backups(baseurl=fote.dr_url, headers=fote.dr_token_header, restore_obj=fote_restore_obj)

def fall_back():
    pass


def switch_over():
    pass


def switch_back():
    pass

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
