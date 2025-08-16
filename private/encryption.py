# private/encryption.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import os

# Generate or load a secret key (16/24/32 bytes for AES)
# Store this key in AWS Secrets Manager or environment variables in production!
SECRET_KEY = os.environ.get('ENCRYPTION_KEY') or b'default_32_byte_key_for_dev_only_1234567890!'  

def encrypt(data: str) -> str:
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(pad(data.encode(), AES.block_size))
    return base64.b64encode(cipher.nonce + tag + ciphertext).decode()

def decrypt(encrypted_data: str) -> str:
    data = base64.b64decode(encrypted_data)
    nonce, tag, ciphertext = data[:16], data[16:32], data[32:]
    cipher = AES.new(SECRET_KEY, AES.MODE_EAX, nonce=nonce)
    return unpad(cipher.decrypt_and_verify(ciphertext, tag), AES.block_size).decode()
