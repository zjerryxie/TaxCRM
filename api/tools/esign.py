from models import IntakeRequest

def send_for_esign(request: IntakeRequest) -> dict:
    # Stub: integrate with DocuSign / HelloSign
    return {"status": "sent", "client": f"{request.first_name} {request.last_name}"}
