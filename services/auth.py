import pyotp

def generate_mfa_secret() -> str:
    return pyotp.random_base32()

def verify_mfa(secret: str, code: str) -> bool:
    totp = pyotp.TOTP(secret)
    return totp.verify(code)
