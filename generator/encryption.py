import secrets
import base64

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_name(name):
    key = secrets.token_bytes(32)
    nonce = secrets.token_bytes(12)

    data = name.encode("utf-8")

    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    combined = key + nonce + ciphertext

    result = base64.urlsafe_b64encode(combined)

    return result.decode("utf-8")

def decrypt_name(code):
    data = code.encode("utf-8")

    combined = base64.urlsafe_b64decode(data)

    key = combined[:32]
    nonce = combined[32: 44]
    ciphertext = combined[44:]
    aesgcm = AESGCM(key)
    name = aesgcm.decrypt(nonce, ciphertext, None)

    return name.decode("utf-8")
