# In models/db.py
from gluon.tools import Auth
auth = Auth(db)
auth.define_tables()

db.define_table('client',
    Field('first_name', 'string'),
    Field('last_name', 'string'),
    Field('email', requires=IS_EMAIL()),
    Field('ssn_last4', 'password'),  # Encrypted storage
    Field('filing_status', requires=IS_IN_SET(['Single', 'MFJ', 'MFS', 'HOH'])),
    Field('tax_year', 'integer', default=2024),
    auth.signature  # Adds created_on/modified_by
)
