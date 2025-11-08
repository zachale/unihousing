#!/bin/bash

# Local deployment script for testing
# Usage: ./deploy.sh [stack-name] [mongo-connection-string]

set -e

STACK_NAME=${1}
MONGO_CONNECTION=${2}

echo "🚀 Deploying Housing Scraper..."
echo "Stack Name: $STACK_NAME"
echo "MongoDB Connection: $MONGO_CONNECTION"

# Build the application
echo "📦 Building application..."
sam build

# Deploy to AWS
echo "☁️  Deploying to AWS..."
sam deploy \
  --stack-name "$STACK_NAME" \
  --parameter-overrides "MongoConnectionString=$MONGO_CONNECTION" \
  --capabilities CAPABILITY_IAM \
  --no-confirm-changeset

# Get outputs
echo "📋 Getting deployment outputs..."
PRODUCER_LAMBDA=$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query 'Stacks[0].Outputs[?OutputKey==`ProducerLambdaFunctionName`].OutputValue' \
  --output text)

CONSUMER_LAMBDA=$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query 'Stacks[0].Outputs[?OutputKey==`ConsumerLambdaFunctionName`].OutputValue' \
  --output text)

QUEUE_URL=$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --query 'Stacks[0].Outputs[?OutputKey==`QueueUrl`].OutputValue' \
  --output text)

echo ""
echo "✅ Deployment successful!"
echo "Producer Lambda: $PRODUCER_LAMBDA"
echo "Consumer Lambda: $CONSUMER_LAMBDA"
echo "Queue URL: $QUEUE_URL"
echo ""
echo "🧪 Test the deployment:"
echo "aws lambda invoke --function-name $PRODUCER_LAMBDA --payload '{}' test.json"