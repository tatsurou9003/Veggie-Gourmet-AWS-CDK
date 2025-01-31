import json
import boto3
import os
from datetime import datetime, timezone, timedelta
import uuid

dynamodb = boto3.resource('dynamodb')
recipe_table = dynamodb.Table(os.environ['RECIPE_TABLE_NAME'])

def post_recipe(event, context):    
    try:
        # CognitoユーザーIDを取得
        user_id = event['requestContext']['authorizer']['claims']['sub']
        
        # リクエストボディからデータを取得
        body = json.loads(event['body'])
        recipe = body['recipe']
        name = body['name']
        ingredients = body['ingredients']
        figure = "https://vegmet-bucket.s3.ap-northeast-1.amazonaws.com/salad.jpg"
        
        # 投稿時刻を追加
        utc_now = datetime.now(timezone.utc)
        jst_now = utc_now.astimezone(timezone(timedelta(hours=9)))
        created_at = jst_now.isoformat()
        
        recipe_table.put_item(
            Item={
                'recipeId': str(uuid.uuid4()),
                'type': "RECIPE",
                'userId': user_id,
                'userName': "匿名",
                'name': name,
                'recipe': recipe,
                'createdAt': created_at,
                'ingredients': ingredients,
                'figure': figure,
                'likesCount': 0
            }
        )

        return {
                'statusCode': 200,
                'body': json.dumps({'message': 'Post created successfully'})
            }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Failed to create post', 'error': str(e)})
        }
