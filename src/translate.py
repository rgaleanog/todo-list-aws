import todoList


def translate(event, context):
    item = todoList.get_item(event['pathParameters']['id'])
    if item:
        result = todoList.translate_item(
            item.get('text'),
            event['pathParameters']['language']
            )
        print('TranslatedText: ' + result.get('TranslatedText'))
        print('SourceLanguageCode: ' + result.get('SourceLanguageCode'))
        print('TargetLanguageCode: ' + result.get('TargetLanguageCode'))
        response = {
            "statusCode": 200,
            "body": result.get('TranslatedText')
        }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response

