# aws_click
 CLI tool in Python 3 to manage ec2 instances on Amazon Web Services

### Installation instructions:
Clone the repository using the following command:
```
git clone https://github.com/Sashamxz/aws_click.git
```

Navigate to the project directory:
```
cd aws_click
```

Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate
```

Install the dependencies listed in the requirements.txt file:
```
pip install -r requirements.txt
```

Add '.env' file in main folder with your data:
```
ACCESS_KEY_ID = 'your key id'
SECRET_ACCESS_KEY = 'your access key'
REGION = 'aws ec2 region'
```

### Usage:
remark:

**instance_id** - it is unique identification for ec2 instance
 
instance_id example ->  i-0114e46wafc2baffq  

To get a list of instances with information about each instance 
use the following command:
```
python3 main.py list 

```
screen1 

Start an instance by ID:

```
python3 main.py start --instance-id your_instance_id

```
screen2 


For a stop instance by ID :

```
python3 main.py stop --instance-id your_instance_id

```
screen3 

Also you can use for stop and start a few ids:
```
python3 main.py stop --instance-id id1 id2 id3
```

### Error Handling

The following is a list of possible errors and their meanings:
_________________________________________________________________________________________________
*No EC2 instance found* : Indicates that there are no EC2 instances available in the account.
_________________________________________________________________________________________________
*No EC2 instance ID provided* : Indicates that an EC2 instance ID was not provided.
_________________________________________________________________________________________________
*EC2 instance with ID {instance_id} is already running* : Indicates that the specified 
                                                      EC2 instance is already in a running state.
_________________________________________________________________________________________________
*EC2 instance with ID {instance_id} is already stopped* : Indicates that the specified 
                                                       EC2 instance is already in a stopped state.
_________________________________________________________________________________________________
*User does not have sufficient permissions to start or stop instance(s)* : check your permission
                                                                    maybe you dont have access
_________________________________________________________________________________________________