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

class CdkVeggieGourmetStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # DynamoDB Table
        recipe_table = dynamodb.Table(self, "RecipeTable",
            partition_key=dynamodb.Attribute(name="recipeId", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="createdAt", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY,
        )

        # GSI（Global Secondary Index）の追加
        recipe_table.add_global_secondary_index(
            index_name="RecipeIndex",
            partition_key=dynamodb.Attribute(name="userId", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="createdAt", type=dynamodb.AttributeType.STRING)
        )

        like_table = dynamodb.Table(self, "LikeTable",
            partition_key=dynamodb.Attribute(name="userId", type=dynamodb.AttributeType.STRING),
            sort_key=dynamodb.Attribute(name="recipeId", type=dynamodb.AttributeType.STRING),
            billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
            removal_policy=RemovalPolicy.DESTROY
        )
        
        # GSI（Global Secondary Index）の追加
        like_table.add_global_secondary_index(
        index_name="RecipeIdIndex",
        partition_key=dynamodb.Attribute(name="recipeId", type=dynamodb.AttributeType.STRING),
        sort_key=dynamodb.Attribute(name="likedAt", type=dynamodb.AttributeType.STRING)
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

        #recipe生成用のLambda関数 
        recipe_lambda = _lambda.Function(
            self, "RecipeLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="recipe.recipe_lambda",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            role = lambda_role
        )
        recipe_integration = apigateway.LambdaIntegration(recipe_lambda)
        recipe_resource = api.root.add_resource("generate-recipe")
        recipe_resource.add_method("GET", recipe_integration)


        #recipe投稿用のLambda関数
        post_lambda = _lambda.Function(
            self, "PostLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="post_recipe.post_recipe",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            environment={
                'POST_TABLE_NAME': recipe_table.table_name,
                'LIKE_TABLE_NAME': like_table.table_name
            }
        )
        post_integration = apigateway.LambdaIntegration(post_lambda)
        post_resource = api.root.add_resource("post-recipe")
        post_resource.add_method("POST", post_integration)

        #recipe投稿用のLambda関数にDynamoDBの権限を付与
        recipe_table.grant_write_data(post_lambda)
        like_table.grant_write_data(post_lambda)


        #recipe全件取得用のLambda関数
        get_lambda = _lambda.Function(
            self, "GetLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="get_recipe.get_recipe",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
        )
        get_integration = apigateway.LambdaIntegration(get_lambda)
        get_resource = api.root.add_resource("get-recipe")
        get_resource.add_method("GET", get_integration)
        
        #recipe全件取得用のLambda関数にDynamoDBの読み取り権限を付与
        recipe_table.grant_read_data(get_lambda)
        like_table.grant_read_data(get_lambda)
