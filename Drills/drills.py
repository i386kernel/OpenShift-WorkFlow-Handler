from OpenShift.VeleroClient.velerohandler import VeleroHandler

restore_obj = {
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


def pre_checks():
    pass


def fail_over() -> None:
    fo = VeleroHandler()
    # fo.scheduleName = "Test_schedule"
    fo.get_backups(fo.dr_url, fo.dr_token_header)
    fo.sort_backups()
    print(fo.restore_scheduled_backups(baseurl=fo.dr_url, headers=fo.dr_token_header, restore_obj=restore_obj))


def failover_test_excercise() -> None:
    fote = VeleroHandler()
    fote.get_backups(fote.dr_url, fote.dr_token_header)
    fote.restore_scheduled_backups(baseurl=fote.dr_url, headers=fote.dr_token_header, restore_obj=restore_obj)


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


velero_getbackups = VeleroHandler()

velero_getbackups.get_backups(baseurl=velero_getbackups.pr_url, headers=velero_getbackups.pr_token_header)
print(velero_getbackups.getallbackups)
