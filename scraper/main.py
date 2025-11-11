import json
import os

import boto3


def lambda_handler(event, context):
    """
    Producer Lambda handler - sends Hello World message to SQS queue
    """
    try:
        # Create SQS client up-front so it's available regardless of which branch we take
        sqs = boto3.client("sqs")

        # Prefer explicit queue URL from environment to avoid GetQueueUrl lookup
        queue_url = os.environ.get("QUEUE_URL")
        # Read queue name (may be None) for diagnostic/response purposes
        queue_name = os.environ.get("QUEUE_NAME")

        if not queue_url:
            # Fallback to queue name and GetQueueUrl for local/dev convenience
            if not queue_name:
                return {
                    "statusCode": 500,
                    "body": json.dumps(
                        {"error": "QUEUE_URL or QUEUE_NAME environment variable not set"}
                    ),
                }
            queue_url_response = sqs.get_queue_url(QueueName=queue_name)
            queue_url = queue_url_response["QueueUrl"]

        # Create the message
        message = {
            "message": "Hello World from Producer Lambda!",
            "timestamp": str(context.aws_request_id) if context else "local",
            "producer_function": context.function_name if context else "local_test",
        }

        # Send message to queue
        response = sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))

        print(f"Message sent to queue. MessageId: {response.get('MessageId')}")

        return {
            "statusCode": 200,
            "body": json.dumps(
                {
                    "message": "Hello World message sent to queue",
                    "message_id": response.get("MessageId"),
                    "queue_name": queue_name,
                    "queue_url": queue_url,
                }
            ),
        }

    except Exception as e:
        print(f"Error sending message to queue: {str(e)}")
        return {"statusCode": 500, "body": json.dumps({"error": str(e)})}
