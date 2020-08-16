import argparse
from VeleroClient.Drills import drills
import os
from DBDataEncoder import dbdataencoder


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

    elif args.command == 'setup':
        dbdataencoder.insert_cred_data(pr_url=args.pr_url, dr_url=args.dr_url, pr_token=args.pr_token,
                                       dr_token=args.dr_token)
        argenvs = [args.pr_url, args.dr_url, args.pr_token, args.dr_token]
        envs = ['PR_URL', 'DR_URL', 'PR_TOKEN', 'DR_TOKEN']
        for idx, argenv in enumerate(argenvs):
            os.environ[envs[idx]] = argenv


if __name__ == "__main__":
    main()
