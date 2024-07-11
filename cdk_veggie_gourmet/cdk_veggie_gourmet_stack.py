from aws_cdk import (
    Duration,
    Stack,
    aws_lambda as _lambda, 
    aws_apigateway as apigateway,
    aws_iam as iam,
    # aws_sqs as sqs,
)
from constructs import Construct

class CdkVeggieGourmetStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

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


        recipe_lambda = _lambda.Function(
            self, "RecipeLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="recipe.recipe_lambda",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
            role = lambda_role
        )

        api =  apigateway.LambdaRestApi(
            self, "VeggieGourmetApi",
            handler=recipe_lambda,
            proxy=True,
        )

        recipe_resource = api.root.add_resource("generate-recipe")
        recipe_resource.add_method("GET")
