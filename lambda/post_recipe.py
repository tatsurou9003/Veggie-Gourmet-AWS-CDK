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
                'partitionKey': "RECIPE",
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
            'body': json.dumps({'message': 'Failed to create post', 'error': str(e)})
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
# 玉ねぎ,ニンジン,レタス,主菜,温かい
# 0
# 普通の野菜スープ
# 野菜を切って出汁で煮込む

# ナス,トマト,キュウリ,主菜,冷たい
# 0
# 塩サラダ
# 野菜をちぎって塩をかける

# ナス,ニンジン,じゃがいも,副菜,冷たい
# 0
# ただの野菜スティック
# 野菜を棒状に切って器にブッ刺す

# 玉ねぎ,トマト,レタス,主菜,冷たい
# 0
# TDNサラダ
# 野菜を切ってドレッシングをぶっかける

# きのこ,トマト,キュウリ,主菜,温かい
# 0
# きのこサラダ
# magic mashroom
