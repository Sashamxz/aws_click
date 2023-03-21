import boto3
from app.config import settings_dict


config = settings_dict['development']


try:
    ec2 = boto3.client(
        'ec2',
        aws_access_key_id=config.ACCESS_KEY_ID,
        aws_secret_access_key=config.SECRET_ACCESS_KEY,
        region_name=config.REGION,
    )

except Exception as e:
    print(f"Connection error: {e}")
