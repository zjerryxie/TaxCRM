# app/services/document_ai.py
import boto3

def extract_w2_data(s3_path: str) -> dict:
    textract = boto3.client('textract')
    response = textract.analyze_document(...)
    return parse_w2_fields(response)  # Your custom parser

def parse_w2_fields(textract_response: dict) -> dict:
    """Extract key W-2 fields (wages, taxes withheld, employer info)."""
    fields = {
        "wages": None,
        "federal_tax_withheld": None,
        "employer_ein": None
    }
    for item in textract_response["Blocks"]:
        if item["BlockType"] == "KEY_VALUE_SET":
            key = item.get("Key", {}).get("Text", "").lower()
            value = item.get("Value", {}).get("Text")
            if "wages" in key: fields["wages"] = float(value)
            elif "federal tax withheld" in key: fields["federal_tax_withheld"] = float(value)
            elif "employer ein" in key: fields["employer_ein"] = value
    return fields

def anonymize_w2_data(w2_data: dict) -> dict:
    """Remove PII before AI processing."""
    return {**w2_data, "employer_ein": None}  # Example
