from models import IntakeRequest

def send_for_esign(request: IntakeRequest) -> dict:
    # Stub: integrate with DocuSign / HelloSign
    return {"status": "sent", "client": f"{request.first_name} {request.last_name}"}


"""
E-signature tool stub
Future: integrate DocuSign / HelloSign for client authorization.
"""

def send_esign_request(client_email: str, document_url: str) -> dict:
    # TODO: Replace with DocuSign/HelloSign API
    return {
        "status": "sent",
        "email": client_email,
        "document_url": document_url,
    }

