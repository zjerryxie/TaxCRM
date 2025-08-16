from docusign_esign import ApiClient, EnvelopesApi

def send_8879(client_email, client_name):
    api_client = ApiClient()
    api_client.host = 'https://demo.docusign.net/restapi'
    api_client.set_default_header("Authorization", "Bearer YOUR_ACCESS_TOKEN")
    
    envelope_api = EnvelopesApi(api_client)
    envelope_definition = {
        "email_subject": "Sign Your IRS Form 8879",
        "recipients": {
            "signers": [{
                "email": client_email,
                "name": client_name,
                "recipient_id": "1"
            }]
        },
        "status": "sent"
    }
    envelope_summary = envelope_api.create_envelope(
        account_id="YOUR_ACCOUNT_ID",
        envelope_definition=envelope_definition
    )
    return envelope_summary.envelope_id
