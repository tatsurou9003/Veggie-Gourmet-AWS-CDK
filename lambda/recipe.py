import json

def recipe_lambda(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello from the recipe lambda",
        }),
    }