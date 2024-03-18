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



sqs = boto3.client(
    'sqs', 
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

s3 = boto3.client(
    's3', 
    region_name=aws_region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

def sendReqtoSQS(image_name):
    queue_url_response = sqs.get_queue_url(QueueName=req_queue_name)
    queue_url = queue_url_response['QueueUrl']
    
    sqs.send_message(QueueUrl=queue_url, MessageBody=image_name)

    #print('Message sent to SQS queue:', req_queue_name)
    
def sendtoS3(image_name, image_file):
    bucket_name = '1230041516-in-bucket'
    s3_key = image_name
    s3.upload_fileobj(image_file, bucket_name, s3_key)
    #print('Image uploaded to S3 successfully')

def receiveResfromSQS(name):
    queue_url_response = sqs.get_queue_url(QueueName=res_queue_name)
    queue_url = queue_url_response['QueueUrl']
    while True:
        response = sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            # WaitTimeSeconds=20,
            VisibilityTimeout=0,
        )
        messages = response.get('Messages',[])
        if messages:
            file_name=messages[0]['Body']
            if(file_name==name):
                receipt_handle = messages[0]['ReceiptHandle']
                classification = get_file_content_from_storage(file_name)
                #print(classification)
                sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
                #print(f"Request processed Successfully")
                # time.sleep(1)
                return classification
        # else:
            #print("No messages in the queue.")
        
def get_file_content_from_storage(file_name):
    response = s3.get_object(Bucket=output_bucket_name, Key=file_name.split('.')[0])
    return response['Body'].read().decode('utf-8')