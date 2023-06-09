import sys
import argparse
from app.service import list_instances, start_instances, stop_instances


# command line argument parser {start, stop, list}
parser = argparse.ArgumentParser(
                                usage=argparse.SUPPRESS,
                                formatter_class=argparse.RawTextHelpFormatter,
                                description='CLI tool in Python that for' +
                                'control EC2 instances on AWS \n\n' +
                                'command example:python3 main.py' +
                                '{start,stop,list} {--all,--instance-id}'
                                )


parser.add_argument('command', nargs='+', choices=['start', 'stop', 'list'],
                    help='The name of the command to execute\n\n' +
                    'command example:  python3 main.py list')

parser.add_argument('--instance-id', dest='instance_ids', nargs='+',
                    help='An EC2 instance ID to operate on \n\n')

parser.add_argument('--all', action='store_true',
                    help='Perform action on all EC2 instances \n\n')


# Command line processing
if __name__ == '__main__':
    args = parser.parse_args()

    instance_ids = args.instance_ids if args.instance_ids is not None else []

    if args.instance_ids and args.all:
        print('Don`t use the --all and --instance-id parameter together')
        quit()

    if args.command[0] == 'start':

        if args.all:
            started = start_instances(all_instances=True)
        else:
            started = start_instances(instance_ids)

        if not started:
            sys.exit(1)

    elif args.command[0] == 'stop':

        if args.all:
            stopped = stop_instances(all_instances=True)
        else:
            stopped = stop_instances(instance_ids)

        if not stopped:
            sys.exit(1)

    elif args.command[0] == 'list':
        list_instances(instance_ids)

    else:
        parser.print_help()
