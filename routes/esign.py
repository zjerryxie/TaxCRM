from docusign_esign import ApiClient, EnvelopesApi

@router.post("/esign/8879")
async def esign_8879(client_id: int):
    client = get_client(client_id)  # Your DB query
    api_client = ApiClient()
    api_client.host = "https://demo.docusign.net/restapi"
    api_client.set_default_header("Authorization", f"Bearer {os.getenv('DOCUSIGN_TOKEN')}")
    
    envelope_api = EnvelopesApi(api_client)
    envelope_definition = {
        "email_subject": "Sign Your IRS Form 8879",
        "recipients": {
            "signers": [{
                "email": client.email,
                "name": client.name,
                "recipient_id": "1"
            }]
        },
        "status": "sent"
    }
    envelope = envelope_api.create_envelope(account_id=os.getenv('DOCUSIGN_ACCOUNT_ID'), envelope_definition=envelope_definition)
    return {"envelope_id": envelope.envelope_id}
