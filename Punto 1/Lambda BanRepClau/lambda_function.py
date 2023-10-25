import json
from urllib import request
import boto3
from datetime import datetime, timedelta

def lambda_handler(event, context):
    # TODO implement
    s3_client = boto3.client('s3')
    
    now = datetime.now() - timedelta(hours=5)
    today = str(now.strftime("%y-%m-%d"))
    
    url = "https://totoro.banrep.gov.co/estadisticas-economicas/rest/consultaDatosService/consultaMercadoCambiario"
    jsondata = request.urlopen(url).read()
    
    s3_client.put_object(Body=jsondata, Bucket='dolar-clau', Key='raw/'+today+'.json')
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
