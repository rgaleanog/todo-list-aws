import json
import decimalencoder
import todoList
import boto3

def get(event, context):
    # create a response
    
    item = todoList.get_item(event['pathParameters']['id'])
    if item:
        response = {
            "statusCode": 200,
            client = boto3.client('translate')
            response = client.translate_text(
                Text=item["text"], 
                SourceLanguageCode='en', 
                TargetLanguageCode='fr' )
            print ('\033[92m' + result.get('TranslatedText') + '\033[0m')
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response