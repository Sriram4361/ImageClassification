import boto3
import time
import os

aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')
aws_region = 'us-east-1'
input_bucket_name="1230041516-in-bucket"
output_bucket_name="1230041516-out-bucket"
res_queue_name="1230041516-resp-queue"
req_queue_name="1230041516-req-queue"
image_id="ami-08230462d0489301b"

ec2_client = boto3.client(
        'ec2',
        region_name=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key)

sqs = boto3.client(
    'sqs', 
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

def get_max_count_of_s3_messages():
    
    s3 = boto3.client(
    's3', 
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)
    
    cur_count=0
    prev_count=0
    rep_count=1
    
    while True:
        response = s3.list_objects_v2(Bucket=input_bucket_name)
        cur_count = response.get('KeyCount', 0)
        if(prev_count==cur_count):
            rep_count+=1
        else:
            rep_count=1
        prev_count=cur_count
        if(rep_count>5 and cur_count>0):
            return cur_count
        print("Approximate number of messages in the s3:", cur_count)
        time.sleep(1)
        
def get_max_count_of_sqs_messages():
    
    cur_count=0
    prev_count=0
    rep_count=1
    
    queue_url_response = sqs.get_queue_url(QueueName=req_queue_name)
    queue_url = queue_url_response['QueueUrl']
    
    while True:
        response = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['ApproximateNumberOfMessages']
            )
        cur_count = int(response['Attributes']['ApproximateNumberOfMessages'])
        if(prev_count==cur_count):
            rep_count+=1
        else:
            rep_count=1
        prev_count=cur_count
        if(cur_count==50 and rep_count>2):
            return cur_count
        elif(rep_count>5 and cur_count>0):
            return cur_count
        print("Approximate number of messages in the queue:", cur_count)
        time.sleep(0.5)

def till_all_messages_consumed():
    queue_url_response = sqs.get_queue_url(QueueName=req_queue_name)
    queue_url = queue_url_response['QueueUrl']
    
    cur_count=0
    prev_count=0
    rep_count=1
    
    while True:
        response = sqs.get_queue_attributes(
            QueueUrl=queue_url,
            AttributeNames=['ApproximateNumberOfMessages']
            )
        cur_count = int(response['Attributes']['ApproximateNumberOfMessages'])
        if(prev_count==cur_count):
            rep_count+=1
        else:
            rep_count=1
        prev_count=cur_count
        if(rep_count>5 and cur_count==0):
            return
    
def purge_sqs_messages():
    queue_url_response = sqs.get_queue_url(QueueName=res_queue_name)
    queue_url = queue_url_response['QueueUrl']
    response = sqs.purge_queue(QueueUrl=queue_url)
    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print("All messages purged from the queue.")
    else:
        print("Failed to purge messages from the queue.")

    
    
def create_ec2_instance(tier_num):
    response = ec2_client.run_instances(
        ImageId=image_id,
        MinCount=1,
        MaxCount=1,
        InstanceType="t2.micro",
        TagSpecifications=[{'ResourceType': 'instance',
                        'Tags': [{
                            'Key': 'Name',
                                   'Value': 'app-tier-instance-'+str(tier_num)}]}]
        )
    instance_id = response['Instances'][0]['InstanceId']
    print(f"Instance {instance_id} created.")
    return instance_id

def terminate_ec2_instances(instance_ids):
    print("-------------------- terminating",target_count," instances-----------------")
    response = ec2_client.terminate_instances(
        InstanceIds=instance_ids
    )
    # for instance in response['TerminatingInstances']:
    #     print(f"Instance {instance['InstanceId']} is in the process of termination.")

def up_instances(target_count, instances):
    print("-------------------- creating",target_count," instances-----------------")
    for i in range(target_count):
        id = create_ec2_instance(i+1)
        instances.append(id)
    return instances


while True:
    req_count=get_max_count_of_sqs_messages()
#     # req_count=get_max_count_of_s3_messages()
    instances=[]
    target_count=2
    if req_count==50:
        target_count=20
    elif req_count>=10:
        target_count=10
    instances=up_instances(target_count, [])
    till_all_messages_consumed()
    if(req_count==50):
        time.sleep(10)
    else:
        time.sleep(5)
    purge_sqs_messages()
    terminate_ec2_instances(instances)
    time.sleep(5)
    
        
        
