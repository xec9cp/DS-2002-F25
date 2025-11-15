#!/usr/bin/ python

import argparse
import requests
import boto3
import os

def download_file(url, local_filename):
    """Download file from URL and save locally."""
    print(f"Downloading file from {url} ...")
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to download file: HTTP {response.status_code}")

    with open(local_filename, "wb") as f:
        f.write(response.content)

    print(f"Saved file to {local_filename}")
    return local_filename


def upload_to_s3(local_filename, bucket, key):
    """Upload a local file to S3."""
    print(f"Uploading {local_filename} to s3://{bucket}/{key} ...")

    s3 = boto3.client("s3")
    s3.upload_file(local_filename, bucket, key, 
                   ExtraArgs={"ContentType": "image/gif","ContentDisposition": "inline"})

    print("Upload complete!")


def presign_url(bucket, key, expiration):
    """Generate a presigned URL for the uploaded file."""
    s3 = boto3.client("s3")
    print(f"Generating presigned URL (expires in {expiration} seconds)...")

    url = s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=expiration
    )

    return url


def main():
    parser = argparse.ArgumentParser(description="Download, upload to S3, and presign a file.")
    parser.add_argument("url", help="URL of the file to download")
    parser.add_argument("bucket", help="S3 bucket name")
    parser.add_argument("--expire", type=int, default=604800, help="Expiration time (seconds), default 7 days")

    args = parser.parse_args()

    filename = os.path.basename(args.url)
    local_path = download_file(args.url, filename)
    upload_to_s3(local_path, args.bucket, filename)
    url = presign_url(args.bucket, filename, args.expire)

    print("\n=== PRESIGNED URL ===")
    print(url)


if __name__ == "__main__":
    main()
