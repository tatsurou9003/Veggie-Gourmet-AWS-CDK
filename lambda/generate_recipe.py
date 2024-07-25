import json
import boto3

def generate_recipe(event, context):
    bedrock_runtime = boto3.client(service_name='bedrock-runtime', region_name='us-east-1')
    model_id = 'anthropic.claude-3-sonnet-20240229-v1:0'
    max_tokens = 600
    system_prompt = "必ず日本語で答えてください。指定した野菜, 主菜or副菜, 温かいor冷たい料理, の条件でレシピを1つ教えてください。"

    body = json.dumps(
        {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": max_tokens,
            "system": system_prompt,
            "messages": [
                {
                    "role": "user",
                    "content": event.get("ingredients")
                }
        ]
        }  
    )  

    response = bedrock_runtime.invoke_model(body=body, modelId=model_id)
    response_body = json.loads(response.get('body').read())

    return {
        'statusCode': 200,
        'body': json.dumps(response_body, ensure_ascii=False)
    }