import json
import boto3
import numpy as np
import pandas as pd
from time import sleep
from datetime import datetime, timedelta
import io
from io import StringIO

def lambda_handler(event, context):
    # TODO implement
    
    endpoint_name = "sagemaker-scikit-learn-2023-10-24-21-01-34-433"

    client = boto3.client("sagemaker-runtime")
    
    tmr = datetime.now() - timedelta(hours=5) + timedelta(days=1) 
    tomorrow = str(tmr.strftime("%Y-%m-%d"))
    
    for i in range(5):
        
        t1 = np.random.randint(4000, 4500)
        t2 = np.random.randint(4000, 4500)
        
        prueba = pd.DataFrame({'fecha':[tomorrow], 't-1': [t1], 't-2': [t2]})
        prueba['fecha'] = pd.to_datetime(prueba['fecha'], format='%Y-%m-%d')
        prueba = prueba.set_index('fecha')
        prueba = prueba.sort_index()
        
        test_file = io.StringIO()
        prueba.to_csv(test_file,header = None, index = None)
        
        response = client.invoke_endpoint(
            EndpointName=endpoint_name,
            Body=test_file.getvalue(),
            InferenceId=str(i),
            ContentType='text/csv',
            Accept='text/csv'
        )
        print(response['Body'].read())
        sleep(1)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
