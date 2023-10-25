import json
import boto3
import numpy as np
import pandas as pd
from time import sleep
from datetime import datetime, timedelta
import random

def lambda_handler(event, context):
    # TODO implement
    
    ground_truth_upload_path = 'dolar/ground_truth'

    client = boto3.client("s3")
    
    NUM_GROUND_TRUTH_RECORDS = 10
    
    def ground_truth_with_id(inference_id):
        random.seed(inference_id)  # to get consistent results
        rand = random.random()
        return {
            "groundTruthData": {
                "data": "1" if rand < 0.7 else "0",  # randomly generate positive labels 70% of the time
                "encoding": "CSV",
            },
            "eventMetadata": {
                "eventId": str(inference_id),
            },
            "eventVersion": "0",
        }
    
    
    def upload_ground_truth(records, upload_time):
        fake_records = [json.dumps(r) for r in records]
        data_to_upload = "\n".join(fake_records)
        target_s3_uri = f"{ground_truth_upload_path}/{upload_time:%Y/%m/%d/%H/%M%S}.jsonl"
        print(f"Uploading {len(fake_records)} records to", target_s3_uri)
        #S3Uploader.upload_string_as_file_body(data_to_upload, target_s3_uri)
        client.put_object(Body=data_to_upload, Bucket='sagemaker-us-east-1-373452244141', Key=target_s3_uri, ContentType='text/html')
        
    def generate_fake_ground_truth_forever():
        j = 0
        while True:
            fake_records = [ground_truth_with_id(i) for i in range(NUM_GROUND_TRUTH_RECORDS)]
            upload_ground_truth(fake_records, datetime.utcnow())
            j = (j + 1) % 5
            sleep(60 * 60)  # do this once an hour
    
    generate_fake_ground_truth_forever()
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
