import json
import decimalencoder
import todoList
import boto3


def translate(event, context):
    # create a response
    available_language=['af','sq','am','ar','hy','az','bn','bs','bg','ca','zh','zh-TW','hr','cs','da','fa-AF','nl','en','et','fa','tl','fi','fr','fr-CA','ka','de','el','gu','ht','ha','he','hi','hu','is','id','ga','it','ja','kn','kk','ko','lv','lt','mk','ms','ml','mt','mr','mn','no','ps','pl','pt','pt-PT','pa','ro','ru','sr','si','sk','sl','so','es','es-MX','sw','sv','ta','te','th','tr','uk','ur','uz','vi','cy']
    item = todoList.get_item(event['pathParameters']['id'])
    code = event['pathParameters']['lang']
    if item and code in available_language:
        translate = boto3.client(service_name='translate',region_name='region')
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