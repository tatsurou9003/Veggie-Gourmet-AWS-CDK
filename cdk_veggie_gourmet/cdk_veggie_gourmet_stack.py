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

        recipe_lambda = _lambda.Function(
            self, "RecipeLambda",
            runtime=_lambda.Runtime.PYTHON_3_12,
            handler="recipe.recipe_lambda",
            code=_lambda.Code.from_asset("lambda"),
            timeout=Duration.seconds(30),
        )

        api =  apigateway.LambdaRestApi(
            self, "VeggieGourmetApi",
            handler=recipe_lambda,
            proxy=True,
        )

        recipe_resource = api.root.add_resource("generate-recipe")
        recipe_resource.add_method("GET")
