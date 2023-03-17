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

###Usage:
remark:

**instance_id** - it is unique identification for ec2 instance

instance_id example ->  i-0114e46wafc2baffq  

To get a list of instances with information about each instance 
use the following command:
For all instances:
```
python3 main.py list  

```
If you need only one , run this command with --instance-id:
```
python3 main.py list  --instance-id your_instance_id
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

Also you can use for stop or start a few ids:
```
python3 main.py stop --instance-id id1 id2 id3
```

### Error Handling

The following is a list of possible errors and their meanings:

First of all if you get an error that starts with **"Connection error"**:
-check your internet connection
-check if you entered the id and key aws access correctly
-check error text

Connection error header:

AccessDeniedException - This error occurs when there are missing or insufficient EC2 access rights.
InvalidSignatureException - This error occurs when the request signature is not valid.
ClientError - This error occurs when there is an interaction error with the EC2 service.
EndpointConnectionError - This error occurs when a connection to the EC2 server cannot be established.
NoCredentialsError - This error occurs when access keys and secret keys are missing.

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
*User does not have sufficient permissions to start or stop instance(s)* : Check your permission,
                                                                    maybe you dont have access.
_________________________________________________________________________________________________
