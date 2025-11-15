#!/bin/bash

set -e

if [ "$#" -lt 2 ]; then
    echo "Usage: $0 <local_file> <bucket_name> [expiration_in_seconds]"
    exit 1
fi

LOCAL_FILE="$1"
BUCKET="$2"
DEFAULT_EXPIRATION=604800 #7 days
EXPIRATION="${3:-$DEFAULT_EXPIRATION}"

FILENAME=$(basename "$LOCAL_FILE")

echo ">>> Uploading $LOCAL_FILE to s3://$BUCKET/$FILENAME ..."
aws s3 cp "$LOCAL_FILE" "s3://$BUCKET/$FILENAME"

echo ">>> Upload complete."

echo ">>> Creating presigned URL (expires in $EXPIRATION seconds)..."
PRESIGNED_URL=$(aws s3 presign "s3://$BUCKET/$FILENAME" --expires-in "$EXPIRATION")

echo ">>> Presigned URL generated:"
echo "$PRESIGNED_URL"
