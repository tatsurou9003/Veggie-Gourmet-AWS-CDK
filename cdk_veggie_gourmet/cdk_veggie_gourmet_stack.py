from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda, 
    aws_apigateway as apigateway,
    aws_iam as iam,
    aws_dynamodb as dynamodb,
    aws_cognito as cognito,
    RemovalPolicy
)
from constructs import Construct
import os
from dotenv import load_dotenv

class CdkVeggieGourmetStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        load_dotenv()
        user_pool_id = os.getenv('USER_POOL_ID')

        # Cognito User Poolを参照
        user_pool = cognito.UserPool.from_user_pool_id(self, "UserPool", user_pool_id)

        # DynamoDB Table
        # ユーザー
        user_table = dynamodb.Table(self, "UserTable",
            partition_key=dynamodb.Attribute(name="userId", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # レシピ1件取得用
        recipe_table = dynamodb.Table(self, "RecipeTable",
            partition_key=dynamodb.Attribute(name="recipeId", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # レシピ全件取得用
        recipe_table.add_global_secondary_index(
            index_name="GetAllIndex",
            partition_key=dynamodb.Attribute(name="type", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="createdAt", type=dynamodb.AttributeType.STRING)
        )

        # ユーザー毎のレシピ取得用
        recipe_table.add_global_secondary_index(
            index_name="UserRecipeIndex",
            partition_key=dynamodb.Attribute(name="userId", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="createdAt", type=dynamodb.AttributeType.STRING)
        )
        
        # いいね
        like_table = dynamodb.Table(self, "LikeTable",
            partition_key=dynamodb.Attribute(name="recipeId", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="likedAt", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # コメント
        comment_table = dynamodb.Table(self, "CommentTable", 
            partition_key=dynamodb.Attribute(name="commentId", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )

        # レシピ毎のコメント取得用
        comment_table.add_global_secondary_index(
            index_name="RecipeCommentIndex",
            partition_key=dynamodb.Attribute(name="recipeId", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="commentedAt", type=dynamodb.AttributeType.STRING)
        )
        
        
        bedrock_policy = iam.PolicyStatement(
            effect= iam.Effect.ALLOW,
            actions= [
                "bedrock:*",   
            ],
            resources= ["*"]
        )

        lambda_role = iam.Role(
            self,
            "RecipeLambdaRole",
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            description="Role to access Bedrock service by lambda",
            managed_policies=[iam.ManagedPolicy.from_aws_managed_policy_name(
                                    'service-role/AWSLambdaBasicExecutionRole'),
                                ]
        )
        lambda_role.add_to_principal_policy(bedrock_policy)

        # REST API
        api =  apigateway.RestApi(
            self, "VeggieGourmetApi",
            rest_api_name="VeggieGourmetApi",
        )

        # Cognitoオーソライザーの作成
        cognito_authorizer = apigateway.CognitoUserPoolsAuthorizer(
            self, "CognitoAuthorizer",
            cognito_user_pools=[user_pool]
        )

        #recipe生成用のLambda関数 
        generate_lambda = _lambda.Function(
            self, "GenerateLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="generate_recipe.generate_recipe",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            role = lambda_role
        )
        generate_integration = apigateway.LambdaIntegration(generate_lambda)
        generate_resource = api.root.add_resource("generate-recipe")
        generate_resource.add_method("POST", generate_integration, authorization_type=apigateway.AuthorizationType.COGNITO, authorizer=cognito_authorizer)


        #recipe投稿用のLambda関数
        post_lambda = _lambda.Function(
            self, "PostLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="post_recipe.post_recipe",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                'RECIPE_TABLE_NAME': recipe_table.table_name,
                'LIKE_TABLE_NAME': like_table.table_name
            }
        )
        post_integration = apigateway.LambdaIntegration(post_lambda)
        post_resource = api.root.add_resource("post-recipe")
        post_resource.add_method("POST", post_integration, authorization_type=apigateway.AuthorizationType.COGNITO, authorizer=cognito_authorizer)

        #recipe投稿用のLambda関数にDynamoDBの権限を付与
        recipe_table.grant_write_data(post_lambda)
        like_table.grant_write_data(post_lambda)


        #recipeページネーション取得用のLambda関数
        get_lambda = _lambda.Function(
            self, "GetLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="get_recipes.get_recipes",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                'RECIPE_TABLE_NAME': recipe_table.table_name,
                'LIKE_TABLE_NAME': like_table.table_name
            }
        )
        get_integration = apigateway.LambdaIntegration(get_lambda)
        get_resource = api.root.add_resource("get-recipes")
        get_resource.add_method("GET", get_integration, authorization_type=apigateway.AuthorizationType.COGNITO, authorizer=cognito_authorizer)
        
        #recipe全件取得用のLambda関数にDynamoDBの読み取り権限を付与
        recipe_table.grant_read_data(get_lambda)
        like_table.grant_read_data(get_lambda)
        

        #recipe削除用のLambda関数
        delete_lambda = _lambda.Function(
            self, "DeleteLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="delete_recipe.delete_recipe",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                'RECIPE_TABLE_NAME': recipe_table.table_name,
                'LIKE_TABLE_NAME': like_table.table_name
            }
        )
