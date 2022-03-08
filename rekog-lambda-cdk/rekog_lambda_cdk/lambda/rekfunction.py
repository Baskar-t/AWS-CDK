import boto3
import json
import os

s3=boto3.client('s3')
rekognition=boto3.client('rekognition')
dynamodb=boto3.client('dynamodb')

def handler(event, context):
    bucket_name = (os.environ['BUCKET_NAME'])
    key = event['Records'][0]['s3']['object']['key']
    image = {
        'S3Object': {
            'Bucket': bucket_name,
            'Name': key
        }
    }

    try:
        response= rekognition.detect_labels(Image= image, MaxLabels=10, MinConfidence=70)
        print(key,response["Labels"])

        # write resuls to JSON file in bucket results folder
        json_labels= json.dumps(response["Labels"])
        filename= os.path.basename(key)
        filename_prefix= os.path.splitext(filename)[0]
        obj= s3.put_object(Body=json_labels, Bucket= bucket_name, Key='results/'+filename_prefix+'.json')

        # parse the JSON for dynamodb update
        db_result = []
        db_labels = json.loads(json_labels)
        for label in db_labels:
            db_result.append(label["Name"])

        # write results to dynamodb
        dynamodb.put_item(TableName=(os.environ['TABLE_NAME']),
            Item = {
                'image_name':{'S': key},
                'labels':{'S':str(db_result)}
            }
        )

        return response
    
    except Exception as e:
        print(e)
        print("Error processing object {} from bucket {}.".format(key, bucket_name))



