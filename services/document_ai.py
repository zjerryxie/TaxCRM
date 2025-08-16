# app/services/document_ai.py
import boto3

def extract_w2_data(s3_path: str) -> dict:
    textract = boto3.client('textract')
    response = textract.analyze_document(...)
    return parse_w2_fields(response)  # Your custom parser
