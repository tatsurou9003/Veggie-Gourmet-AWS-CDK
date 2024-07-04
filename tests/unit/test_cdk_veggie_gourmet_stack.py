import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_veggie_gourmet.cdk_veggie_gourmet_stack import CdkVeggieGourmetStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_veggie_gourmet/cdk_veggie_gourmet_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkVeggieGourmetStack(app, "cdk-veggie-gourmet")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
