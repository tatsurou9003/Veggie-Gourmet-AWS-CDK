# import json
# import decimal
# from boto3.dynamodb.conditions import Key, Attr
# import boto3

# dynamodb = boto3.resource('dynamodb')

# class DecimalEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, decimal.Decimal):
#             return float(obj)
            
#         return super(DecimalEncoder, self).default(obj)

# def lambda_handler(event, context):
#     table = dynamodb.Table('Recipe')
#     response = table.scan()
#     items = response['Items']

#     return {
#         'isBase64Encoded': False,
#         'statusCode': 200,
#         'headers': {
#             'Content-Type': 'application/json',
#             # CORS ヘッダーを追加
#             'Access-Control-Allow-Origin': '*',  # 特定のドメインに変更してください
#             'Access-Control-Allow-Methods': 'GET,　OPTIONS', # 必要なメソッドに応じて
#             'Access-Control-Allow-Headers': 'Content-Type,Authorization' # 必要に応じて
#         },
#         'body': json.dumps(items, ensure_ascii=False, cls=DecimalEncoder)
#     }
