import json
import decimalencoder
import todoList
import boto3


def translate(event, context):
    # create a response
    item = todoList.get_item(event['pathParameters']['id'])
    code = event['pathParameters']['lang']
    if item:
        translate = boto3.client(
                service_name='translate',
                region_name='region'
        )
        result = translate.translate_text(
            Text=item,
            SourceLanguageCode='auto',
            TargetLanguageCode=code
        )
        response = {
            "statusCode": 200,
            "body": json.dumps(result['TranslatedText'],
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response
