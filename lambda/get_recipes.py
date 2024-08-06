import json
from decimal import Decimal
import os
from boto3.dynamodb.conditions import Key
import boto3

dynamodb = boto3.resource('dynamodb')
recipe_table = dynamodb.Table(os.environ['RECIPE_TABLE_NAME'])

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError

# DynamoDBのテーブル定義で、同時刻（コンマ数秒）のデータが複数ある場合エラーになるという致命的なバグがある。
# scanの方が確実だが、パフォーマンス上の問題があるため、今回はqueryを使用する。個人開発だし。
def get_recipes(event, context):
    try:
        query_string_parameters = event.get('queryStringParameters')
        exclusive_start_key = None
        index_name="RecipeIndex"
        
        if query_string_parameters:
            exclusive_start_key = query_string_parameters.get('lastEvaluatedKey')
            
        query_params = {
            'IndexName': index_name,
            'KeyConditionExpression': Key('partitionKey').eq('RECIPE'),
            'ScanIndexForward': False,
            'Limit': 5
        }
        
        if exclusive_start_key:
            query_params['ExclusiveStartKey'] = json.loads(exclusive_start_key)
        
        response = recipe_table.query(**query_params)
        print(response)
        
        items = response.get('Items', [])
        last_evaluated_key = response.get('LastEvaluatedKey')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'recipes': items,
                'lastEvaluatedKey': last_evaluated_key
            }, default=decimal_default, ensure_ascii=False),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
