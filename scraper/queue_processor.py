import json
import boto3

def lambda_handler(event, context):
    """
    AWS Lambda handler that processes messages from SQS queue
    """
    print(f"Received event: {json.dumps(event)}")

    # Process each record in the SQS event
    for record in event.get('Records', []):
        try:
            # Parse the SQS message body
            message_body = record['body']
            print(f"Processing message: {message_body}")

            # Parse the message if it's JSON
            try:
                message_data = json.loads(message_body)
            except json.JSONDecodeError:
                message_data = message_body

            # Process the message (in this case, just log it)
            if isinstance(message_data, dict) and 'message' in message_data:
                print(f"Hello from consumer: {message_data['message']}")
            else:
                print(f"Received message: {message_data}")

            # Here you could add your scraper processing logic
            # For example, call builder() and crawler() functions

            print("Message processed successfully")

        except Exception as e:
            print(f"Error processing message: {str(e)}")
            # In a real application, you might want to send failed messages to a dead letter queue
            raise e

    return {
        'statusCode': 200,
        'body': json.dumps({
            'message': 'Successfully processed queue messages',
            'message_count': len(event.get('Records', []))
        })
    }

