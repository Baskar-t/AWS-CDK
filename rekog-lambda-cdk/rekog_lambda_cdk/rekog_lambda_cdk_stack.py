from aws_cdk import (
    aws_iam as iam,
    aws_lambda as _lambda,
    aws_s3 as s3,
    aws_dynamodb as ddb,
    aws_s3_notifications as s3_notify,
    Stack
)

from constructs import Construct

class RekogLambdaCdkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create IAM user and group
        group = iam.Group(self, "Developer")
        user  = iam.User(self, "Baskar")

        group.add_user(user)

        # create S3 bucket to hold images
        # give new user access to the bucket

        bucket = s3.Bucket(self, "Bucket")
        bucket.grant_read_write(user)

         # create DynamoDB table to hold Rekognition results
        table = ddb.Table(self,"classification",
            partition_key={'name': 'image_name', 'type': ddb.AttributeType.STRING}        
        )

        # create Lambda function
        lambda_function = _lambda.Function(self, 'Rekfunction',
            runtime= _lambda.Runtime.PYTHON_3_7,
            code= _lambda.Code.from_asset('rekog_lambda_cdk/lambda'),   
            handler='rekfunction.handler',
            environment={
               'BUCKET_NAME' : bucket.bucket_name,
               'TABLE_NAME'  : table.table_name
            }
                   
        )

        # add recog permission for lambda function
        statement= iam.PolicyStatement()
        statement.add_actions("rekognition:DetectLabels")
        statement.add_resources("*")
        lambda_function.add_to_role_policy(statement)

        # create trigger for lambda function
        notifications= s3_notify.LambdaDestination(lambda_function)
        notifications.bind(self, bucket)
        bucket.add_object_created_notification(notifications, s3.NotificationKeyFilter(suffix='.jpg'))
        bucket.add_object_created_notification(notifications, s3.NotificationKeyFilter(suffix='.jpeg'))
        bucket.add_object_created_notification(notifications, s3.NotificationKeyFilter(suffix='.png'))

        table.grant_read_write_data(lambda_function)
        bucket.grant_read_write(lambda_function)



        




