import time
from prettytable import PrettyTable
from tqdm import tqdm
from app.connection import ec2


# check user permission
# def check_permissions(instance_ids):
#     for instance_id in instance_ids:
#         response = (
#             ec2.describe_instance_attribute(InstanceId=instance_id,
#                                             Attribute='disableApiTermination')
#         )

#         for attribute in response['DisableApiTermination']['Value']:
#             if attribute['Value'] is True:
#                 print(f'User does not have sufficient permissions to \
#                       start or stop instance {instance_id}')
#                 return False
#     return True


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

    if all_instances:
        instance_list = get_instance_list()
        instance_ids = [instance['InstanceId'] for instance in instance_list
                        if instance['State']['Name'] != 'running']

    if not instance_ids:
        print('No EC2 instance ID provided')
        return

    # Check user permissions
    # if not check_permissions(instance_ids,'start'):
    #     return

    for instance_id in instance_ids:

        instance = get_instance_by_id(instance_id)

        if instance['State']['Name'] == 'running':
            print(f'EC2 instance with ID {instance_id} is already running')
            if len(instance_ids) == 1:
                return
            continue

        for i in tqdm(range(100), desc=f'Starting instance- {instance_id}'):
            ec2.start_instances(InstanceIds=[instance_id])
            time.sleep(0.5)
        print()

    print(f'EC2 instance with ID {", ".join(instance_ids)} was started')


# stop ec2 instance(s)
def stop_instances(instance_ids=None, all_instances=False):

    if all_instances:
        instance_list = get_instance_list()
        instance_ids = [instance['InstanceId'] for instance in instance_list
                        if instance['State']['Name']
                        not in ['stopped', 'stopping']]

    if not instance_ids:
        print('No EC2 instance ID provided')
        return

    # Check user permissions
    # if not check_permissions(instance_ids):
    #     return

    for instance_id in instance_ids:

        instance = get_instance_by_id(instance_id)

        if instance['State']['Name'] in ['stopped', 'stopping']:
            print(f'EC2 instance with ID {instance_id} is already stoped')
            if len(instance_ids) == 1:
                return
            continue

        for i in tqdm(range(100), desc=f'Stoping instance-{instance_id}'):
            ec2.stop_instances(InstanceIds=[instance_id])
            time.sleep(0.5)
        print()

    print(f'EC2 instance with ID {", ".join(instance_ids)} was stopped')
