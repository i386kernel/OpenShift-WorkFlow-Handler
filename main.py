import argparse
import os
from VeleroClient.Drills import drills
from DBDataEncoder import dbdataencoder
import presets


def main():
    parser = argparse.ArgumentParser(description='Executes Drills in Openshift Environment with Velero Operator')
    subparser = parser.add_subparsers(dest="command")

    # Sub-Parser for Execute Operations
    execute_parser = subparser.add_parser('execute', help='Execute Drills for Openshift')
    execute_parser.add_argument('-vd', '--vdrill', help='Perform Drill', type=str,
                                choices=['fo', 'fote', 'fb', 'sw', 'sb'], required=True, dest='velero_drill')
    execute_parser.add_argument('-vs', '--vschedule', help='Schedule to Restore', type=str, required=True,
                                dest='velero_schedule_name')

    # Initial Setup of Openshift Work-Flow Container Sub-Parser
    setup_parser = subparser.add_parser('setup', help='Setup Initial OpenShift Work-Flow Container')
    setup_parser.add_argument('-pu', '--prurl', help='PR URL', type=str, required=True, dest='pr_url')
    setup_parser.add_argument('-du', '--drurl', help='DR URL', type=str, required=True, dest='dr_url')
    setup_parser.add_argument('-pt', '--prtoken', help='PR Service Token', type=str, required=True, dest='pr_token')
    setup_parser.add_argument('-dt', '--drtoken', help='DR Service Token', type=str, required=True, dest='dr_token')
    args = parser.parse_args()

    # Execute appropriate drills
    if args.command == 'execute':
        if args.velero_drill == 'fo':
            drills.fail_over(schedule=args.velero_schedule_name)
        elif args.velero_drill == 'fote':
            drills.failover_test_excercise(schedule=args.velero_schedule_name)
        elif args.velero_drill == 'fb':
            drills.fall_back()
        elif args.velero_drill == 'so':
            drills.switch_over()
        elif args.velero_drill == 'sb':
            drills.switch_back()

    # Initiate Setup
    elif args.command == 'setup':
        # if os.path.exists(presets.DATA_PATH + "/opworkflowmanager.db"):
        #     os.remove(presets.DATA_PATH+"/opworkflowmanager.db")
        #     dbdataencoder.insert_cred_data(pr_url=args.pr_url, dr_url=args.dr_url, pr_token=args.pr_token,
        #                                    dr_token=args.dr_token)
        #     drills.pre_checks()
        # else:
            dbdataencoder.insert_cred_data(pr_url=args.pr_url, dr_url=args.dr_url, pr_token=args.pr_token,
                                           dr_token=args.dr_token)
            drills.pre_checks()


if __name__ == "__main__":
    main()
