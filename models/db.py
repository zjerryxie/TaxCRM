# models/db.py
from gluon.tools import Auth
auth = Auth(db)
auth.define_tables()

# Import encryption (Web2py auto-loads modules in modules/)
from encryption import encrypt, decrypt

db.define_table('client',
    Field('first_name'),
    Field('last_name'),
    Field('ssn_last4', 'password',  # Uses Web2py's built-in password hashing (not ideal for SSN)
    # OR use custom encryption:
    Field('ssn_encrypted', 'text'),  # Store ciphertext here
    # ...
)

# Example: Automatically encrypt SSN before saving
def encrypt_ssn_callback(row):
    if row.ssn_last4:  # If using plaintext field
        row.ssn_encrypted = encrypt(row.ssn_last4)
    return row

db.client._before_insert.append(encrypt_ssn_callback)
db.client._before_update.append(encrypt_ssn_callback)
