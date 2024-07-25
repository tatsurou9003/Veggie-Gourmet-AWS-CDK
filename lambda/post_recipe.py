import json
import boto3
import os
import pytz
from datetime import datetime
import uuid

dynamodb = boto3.resource('dynamodb')
recipe_table = dynamodb.Table(os.environ['RECIPE_TABLE_NAME'])

def post_recipe(event, context):    
    try:
        # CognitoユーザーIDを取得
        user_id = event['requestContext']['authorizer']['claims']['sub']
        
        # リクエストボディからデータを取得
        body = json.loads(event['body'])
        recipe_id = str(uuid.uuid4())
        recipe = body['recipe']
        name = body['name']
        ingredients = body['ingredients']
        figure = "https://vegmet-bucket.s3.ap-northeast-1.amazonaws.com/salad.jpg"
        
        # 投稿時刻を追加
        utc_now = datetime.now().isoformat()
        jst = pytz.timezone('Asia/Tokyo')
        jst_now = utc_now.replace(tzinfo=pytz.utc).astimezone(jst)
        created_at = jst_now.isoformat()

        recipe_table.put_item(
            Item={
                'recipeId': recipe_id,
                'userId': user_id,
                'recipe': recipe,
                'createdAt': created_at,
                'name': name,
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
            'body': json.dumps({'message': 'Failed to create post'})
        }


# eventの中身(生成したrecipeのテキストにFlutterがパラメータを付加したもの)
# {
#   "recipe_id": "11111",
#   "user_id": "22222",　// user_id = event['requestContext']['authorizer']['claims']['sub']
#   "recipe": "salt, pepper, and so on.",
#   "created_at": "2022-01-01T00:00:00"
#   "like_count": 0,
#   "name": "veggietable burger",
#   "ingredients": "tomato,cucumber,eggplant",
#   "figure": "https://vegmet-bucket.s3.ap-northeast-1.amazonaws.com/salad.jpg",
# }
