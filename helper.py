import boto3
import os

# Specify your AWS credentials
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = 'us-east-1'


ec2_client = boto3.resource(
    'ec2',
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)


ami_id = "ami-00ddb0e5626798373"
instance = ec2_client.create_instances(
    ImageId=ami_id,
    MinCount=1,
    MaxCount=1,
    InstanceType="t2.micro",
    KeyName='project',
    TagSpecifications=[{'ResourceType': 'instance',
                        'Tags': [{
                            'Key': 'Name',
                                   'Value': 'WebTier'}]}])
