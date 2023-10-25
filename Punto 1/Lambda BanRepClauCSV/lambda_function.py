import json
from urllib import request
import boto3
import pandas as pd
from datetime import datetime, timedelta
from io import StringIO

def lambda_handler(event, context):
    # TODO implement
    s3_client = boto3.client('s3')
    
    now = datetime.now() - timedelta(hours=5) 
    today = str(now.strftime("%y-%m-%d"))
    
    s3_response = s3_client.get_object(
        Bucket='dolar-clau',
        Key='raw/'+today+'.json'
    )
    
    s3_object_body = s3_response.get('Body')
    
    content = s3_object_body.read()
    
    json_dict = json.loads(content)
    csvdata = pd.DataFrame(json_dict)
    
    df = pd.DataFrame(csvdata)
    df.columns =['fecha','precio']
    df['fecha'] = pd.to_datetime(df['fecha'], unit='ms')
    df['fecha'] = pd.to_datetime(df['fecha']).dt.strftime('%d/%m/%Y %H:%M:%S')
    
    bucket = 'dolar-clau-final'
    csv_buffer = StringIO()
    df.to_csv(csv_buffer,index=False)
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, 'final/'+today+'.csv').put(Body=csv_buffer.getvalue())
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
