import argparse
from service import list_instances, start_instances, stop_instances, \
                    get_instance_list


# command line argument parser
parser = argparse.ArgumentParser(description='CLI tool in Python that can be \
                                 used to control EC2 instances on AWS')

parser.add_argument('command', nargs='+', choices=['start', 'stop', 'list'],
                    help='The name of the command to execute')

parser.add_argument('--instance-id', dest='instance_ids', nargs='+',
                    help='An EC2 instance ID to operate on')

# Command line processing
args = parser.parse_args()

instance_ids = args.instance_ids or []

if args.command[0] == 'start':
    if args.instance_ids:
        instance_ids = args.instance_ids
    else:
        instances = get_instance_list()
        if instances:
            instance_ids = [instances[0]['InstanceId']]
        else:
            print('No EC2 instances found')
            exit()

    start_instances(instance_ids)

elif args.command[0] == 'stop':
    stop_instances(instance_ids)

elif args.command[0] == 'list':
    list_instances(instance_id=instance_ids)

else:
    parser.print_help()
