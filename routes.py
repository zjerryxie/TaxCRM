import boto3
from flask import current_app

def upload_to_s3(file, client_id):
    s3 = boto3.client(
        's3',
        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
        aws_secret_access_key=current_app.config['AWS_SECRET_KEY']
    )
    s3.upload_file(
        file, 
        'your-taxcrm-bucket', 
        f'clients/{client_id}/{file.filename}'
    )
    return f"s3://your-taxcrm-bucket/clients/{client_id}/{file.filename}"
