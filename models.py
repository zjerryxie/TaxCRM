from app import db
from werkzeug.security import generate_password_hash

class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    # --- Tax-Specific Additions ---
    ssn_last4 = db.Column(db.String(4))  # Store encrypted (see Step B)
    filing_status = db.Column(db.String(20))  # 'Single', 'MFJ', 'HOH', etc.
    tax_year = db.Column(db.Integer, default=2024)

class TaxDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    doc_type = db.Column(db.String(20))  # 'W-2', '1099', '8879'
    file_path = db.Column(db.String(200))  # Store encrypted in S3 (see Step C)
    status = db.Column(db.String(20))  # 'Received', 'Reviewed', 'Filed'
