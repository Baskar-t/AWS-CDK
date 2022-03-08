import json

def handler(event, context):
    print ('request: {}'.format(json.dumps(event)))
    return {
        'statusCode': 200,
        'headers': {
            'context-Type': 'text/plain'
        },
        'body' : 'Good night, CDk! You have hit {}'.format(event['path'])
        
    }