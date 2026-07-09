from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import os

KEY_FILE = "aes.key"

#  Create AES key ONCE
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "wb") as f:
        f.write(get_random_bytes(16))  # 16 bytes = 128-bit AES

#  Load AES key
with open(KEY_FILE, "rb") as f:
    AES_KEY = f.read()

#  SAFETY CHECK
if len(AES_KEY) not in (16, 24, 32):
    raise RuntimeError(f"Invalid AES key length: {len(AES_KEY)} bytes")


def encrypt_message(message: str) -> str:
    cipher = AES.new(AES_KEY, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    return base64.b64encode(
        cipher.nonce + tag + ciphertext
    ).decode()


def decrypt_message(encrypted_message: str) -> str:
    data = base64.b64decode(encrypted_message)

    nonce = data[:16]
    tag = data[16:32]
    ciphertext = data[32:]

    cipher = AES.new(AES_KEY, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    return plaintext.decode()

print("AES KEY LENGTH:", len(AES_KEY))
