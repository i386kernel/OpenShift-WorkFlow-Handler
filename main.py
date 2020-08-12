import argparse
from VeleroClient.Drills import drills
import os


def main():
    parser = argparse.ArgumentParser(description='Executes Drills in Openshift Environment with Velero Operator')
    parser.add_argument('-vd', '--vdrill', help='Perform Drill', type=str, choices=['fo', 'fote', 'fb', 'sw', 'sb'],
                        required=True, dest='velero_drill')
    parser.add_argument('-vs', '--vschedule', help='Schedule to Restore', type=str, required=True,
                        dest='velero_schedule_name')
    parser.add_argument('-pu', '--prurl', help='PR URL', type=str, required=False, dest='pr_url')
    parser.add_argument('-du', '--drurl', help='DR URL', type=str, required=False, dest='dr_url')
    parser.add_argument('-pt', '--prtoken', help='PR Service Token', type=str, required=False, dest='pr_token')
    parser.add_argument('-dt', '--drtoken', help='DR Service Token', type=str, required=False, dest='dr_token')
    args = parser.parse_args()

    argenvs = [args.pr_url, args.dr_url, args.pr_token, args.dr_token]
    envs = ['PR_URL', 'DR_URL', 'PR_TOKEN', 'DR_TOKEN']

    for idx, argenv in enumerate(argenvs):
        if argenv:
            os.environ[envs[idx]] = argenv

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


if __name__ == "__main__":
    main()
