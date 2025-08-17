import boto3
import os

def generate_presign_url(filename: str, operation: str = "upload") -> str:
    s3 = boto3.client("s3")
    bucket = os.getenv("S3_BUCKET", "my-taxcrm-bucket")

    try:
        if operation == "upload":
            return s3.generate_presigned_url(
                "put_object",
                Params={"Bucket": bucket, "Key": filename},
                ExpiresIn=3600
            )
        elif operation == "download":
            return s3.generate_presigned_url(
                "get_object",
                Params={"Bucket": bucket, "Key": filename},
                ExpiresIn=3600
            )
    except Exception as e:
        print("Error generating presign URL:", e)
        return None
