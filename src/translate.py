import json
import decimalencoder
import todoList
import boto3

def translate(event, context):
    # create a response
    item = todoList.get_item(event['pathParameters']['id'])
    code = event['pathParameters']['lang']
    if item:
        response = {
            "statusCode": 200,
            "body": json.dumps(item + code,
                               cls=decimalencoder.DecimalEncoder)
        }
        else:
            response = {
                "statusCode": 404,
                "body": ""
            }
            return response
