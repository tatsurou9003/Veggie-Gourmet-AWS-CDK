import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
post_table = dynamodb.Table(os.environ['POST_TABLE_NAME'])
like_table = dynamodb.Table(os.environ['LIKE_TABLE_NAME'])

def post_recipe(event, context):    
    return {
        'statusCode': 200,
        'body': json.dumps({'message': '${post_table} ${like_table}'})
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

# テスト用JWTトークン取得コマンド
# aws cognito-idp initiate-auth \
#     --auth-flow USER_PASSWORD_AUTH \
#     --client-id exampleclientid \
#     --auth-parameters USERNAME=user@example.com,PASSWORD=examplepassword
