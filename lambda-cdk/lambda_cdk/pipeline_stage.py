from constructs import Construct
from aws_cdk import (
    Stage
)
from lambda_cdk.lambda_cdk_stack import LambdaCdkStack

class WorkshopPipelineStage(Stage):

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = LambdaCdkStack(self, 'WebService')