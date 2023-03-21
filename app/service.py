import sys
from prettytable import PrettyTable
from tqdm import tqdm
from app.connection import ec2
from botocore.exceptions import ClientError


# check user permissions
def check_permission(action, instance_id):
    try:
        if action == 'start':
            ec2.start_instances(InstanceIds=[instance_id], DryRun=True)
        elif action == 'stop':
            ec2.stop_instances(InstanceIds=[instance_id], DryRun=True)
        return True
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            print(f'Client error : {e}')
            return False
        else:
            return True


# get instance by ID
def get_instance_by_id(instance_id):
    instance = (
        ec2.describe_instances(InstanceIds=[instance_id])
        ['Reservations'][0]
        ['Instances'][0]
    )
    return instance


# get all instances for parsing
def get_instance_list():
    response = ec2.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance)
    return instances


# show all instances in table with
# rows 'PK','ID','Name','State','Type','Region'
def list_instances(instance_id=None):
    if instance_id:
        instances = (
            ec2.describe_instances(InstanceIds=instance_id)
            ['Reservations'][0]
            ['Instances']
        )
    else:
        instances = get_instance_list()

    if not instances:
        print('No EC2 instance(s) found')
    else:
        table = PrettyTable(['PK', 'ID', 'Name', 'State', 'Type', 'Region'])
        for pk, instance in enumerate(instances, start=1):

            instance_name = next(
               (tag['Value'] for tag in instance['Tags']
                if tag['Key'] == 'Name'), ''
            )
            instance_id = instance['InstanceId']
            table.add_row([pk, instance_id, instance_name,
                           instance['State']['Name'],
                           instance['InstanceType'],
                           instance['Placement']['AvailabilityZone']])
        print(table)


# start ec2 instance(s)
def start_instances(instance_ids=None, all_instances=False):

    # if we use command 'start' with '--all'
    if all_instances:
        instance_list = get_instance_list()
        instance_ids = [instance['InstanceId'] for instance in instance_list
                        if instance['State']['Name'] != 'running']
        if not instance_ids:
            print('No instances available for starting')
            sys.exit()

    # if we use start --instance-id id1 id2 ...
    if not instance_ids:
        print('No EC2 instance ID provided')
        sys.exit()

    started_instances = []
    for instance_id in instance_ids:
        instance = get_instance_by_id(instance_id)

        if instance['State']['Name'] == 'running':
            print(f'EC2 instance with ID {instance_id} is already running')
            if len(instance_ids) == 1:
                exit()
            continue

        # Check user permissions
        if not check_permission('start', instance_id):
            print('User does not have sufficient permissions for'
                  ' starting the instance')
            continue

        for i in tqdm(range(100), desc=f'Starting instance- {instance_id}'):
            ec2.start_instances(InstanceIds=[instance_id])
        started_instances.append(instance_id)
        print()

    if started_instances:
        print(f'EC2 instance with ID {", ".join(started_instances)}'
              ' was started')
    else:
        print('No instances were started')


# stop ec2 instance(s)
def stop_instances(instance_ids=None, all_instances=False):

    # if we use command 'start' with '--all'
    if all_instances:
        instance_list = get_instance_list()
        instance_ids = [instance['InstanceId'] for instance in instance_list
                        if instance['State']['Name']
                        not in ['stopped', 'stopping']]
        if not instance_ids:
            print('No instances available for stopping')
            sys.exit()

    # if we use command 'start' with '--instance-id'
    elif not instance_ids:
        print('No EC2 instance ID provided')
        sys.exit()

    stopped_instances = []

    for instance_id in instance_ids:

        instance = get_instance_by_id(instance_id)

        if instance['State']['Name'] in ['stopped', 'stopping']:
            print(f'EC2 instance with ID {instance_id} is already stopped \n')
            # if we had only one instance in list , which is already stopped
            if len(instance_ids) == 1:
                sys.exit()
            continue

        # Check user permissions
        if not check_permission('stop', instance_id):
            print('User does not have sufficient permissions for'
                  ' stopping the instance')
            continue

        for i in tqdm(range(100), desc=f'Stopping instance-{instance_id}'):
            ec2.stop_instances(InstanceIds=[instance_id])
        stopped_instances.append(instance_id)
        print()

    if stopped_instances:
        print(f'EC2 instance with ID {", ".join(stopped_instances)}'
              ' was stopped')
    else:
        print('No instances were stopped')
