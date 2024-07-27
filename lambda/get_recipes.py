import json
import os
from boto3.dynamodb.conditions import Key
import boto3

dynamodb = boto3.resource('dynamodb')
recipe_table = dynamodb.Table(os.environ['RECIPE_TABLE_NAME'])

def get_recipes(event, context):
    try:
        exclusive_start_key = event.get('queryStringParameters', {}).get('lastEvaluatedKey')
        query_params = {
            'KeyConditionExpression': Key('recipeId').begins_with('RECIPE#'),
            'ScanIndexForward': False,
            'Limit': 10
        }
        
        if exclusive_start_key:
            query_params['ExclusiveStartKey'] = json.loads(exclusive_start_key)
        
        response = recipe_table.query(**query_params)
        
        items = response.get('Items', [])
        last_evaluated_key = response.get('LastEvaluatedKey')
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'recipes': items,
                'lastEvaluatedKey': last_evaluated_key
            }),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': 'Internal Server Error'}),
            'headers': {
                'Content-Type': 'application/json'
            }
        }
