import json
import decimalencoder
import todoList


def get(event, context):
    # create a response
    item = todoList.get_item(event['pathParameters']['id'])
    lang = event['pathParameters']['lang']

    if item:
        item['text'] = todoList.translate(item['text'], lang)
        
        response = {
            "statusCode": 200,
            "body": json.dumps(item,
                               cls=decimalencoder.DecimalEncoder)
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response
