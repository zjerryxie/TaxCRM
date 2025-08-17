import os

# Centralized config for environment variables
S3_BUCKET = os.getenv("S3_BUCKET", "your-default-bucket")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Auth (for future use, OIDC/JWT provider)
OIDC_ISSUER = os.getenv("OIDC_ISSUER", "https://your-issuer.com")
OIDC_CLIENT_ID = os.getenv("OIDC_CLIENT_ID", "your-client-id")

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
