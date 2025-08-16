import boto3
from fastapi import UploadFile

def upload_to_s3(file: UploadFile, client_id: int) -> str:
    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET')
    )
    s3.upload_fileobj(
        file.file,
        'your-taxcrm-bucket',
        f'clients/{client_id}/{file.filename}',
        ExtraArgs={'ServerSideEncryption': 'AES256'}
    )
    return f"s3://your-taxcrm-bucket/clients/{client_id}/{file.filename}"
