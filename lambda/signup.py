import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table(os.environ['USER_TABLE_NAME'])

def signup(event, context):
    try:
        user_id = event['requestContext']['authorizer']['claims']['sub']
        body = json.loads(event['body'])
        username = body['username']
        profile = None
        picture = None

        user_table.put_item(
            Item={
                'userId': user_id,
                'username': username,
                'profile': profile,
                'picture': picture
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User created successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to create user', 'error': str(e)})
        }
    