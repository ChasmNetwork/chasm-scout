#!/bin/sh

# Load the .env file
export $(grep -v '^#' .env | xargs)

# Check if WEBHOOK_API_KEY is set
if [ -z "$WEBHOOK_API_KEY" ]; then
  echo "WEBHOOK_API_KEY is not set in the .env file"
  exit 1
fi

# Check if WEBHOOK_URL is set
if [ -z "$WEBHOOK_URL" ]; then
  echo "WEBHOOK_URL is not set in the .env file"
  exit 1
fi

# Make a POST request using curl to 3001 with authorization
curl -X POST \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer $WEBHOOK_API_KEY" \
     -d '{"body":"{\"model\":\"gemma2-9b-it\",\"messages\":[{\"role\":\"system\",\"content\":\"You are a helpful assistant.\"}]}"}' \
     $WEBHOOK_URL
