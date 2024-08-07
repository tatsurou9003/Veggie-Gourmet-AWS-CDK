import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table(os.environ['USER_TABLE_NAME'])