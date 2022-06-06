import todoList


def translate(event, context):
    item = todoList.get_item(event['pathParameters']['id'])
    if item:
        try:
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
        except Exception as e:
            print('esto es una exception')
            print(e)
            response = {
                "statusCode": 400,
                "body": str(e)
            }
    else:
        response = {
            "statusCode": 404,
            "body": ""
        }
    return response
