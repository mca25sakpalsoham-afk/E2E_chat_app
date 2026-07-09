import time
from crypto.crypto_utils import encrypt_message, decrypt_message
import base64

# ===============================
# 1. Encryption Integrity Test
# ===============================

def run_encryption_integrity_check():
    start = time.time()

    try:
        original = "This is a secure test message"

        encrypted = encrypt_message(original)
        decrypted = decrypt_message(encrypted)

        end = time.time()
        duration = round((end - start) * 1000, 3)  # ms

        if decrypted == original:
            return {
                "status": "PASS",
                "time": duration,
                "details": "AES encryption, MAC, and decryption verified"
            }
        else:
            return {
                "status": "FAIL",
                "time": duration,
                "details": "Decrypted message does not match original"
            }

    except Exception as e:
        end = time.time()
        duration = round((end - start) * 1000, 3)

        return {
            "status": "FAIL",
            "time": duration,
            "details": f"Exception occurred: {str(e)}"
        }


# ===============================
# 2. Message Tampering Test
# ===============================

def message_tampering_test():
    start = time.time()

    try:
        original = "This message will be tampered"
        encrypted = encrypt_message(original)

        # Decode base64 → bytes
        raw = base64.b64decode(encrypted)

        # Tamper last byte
        tampered = raw[:-1] + bytes([raw[-1] ^ 1])

        tampered_b64 = base64.b64encode(tampered).decode()

        # This SHOULD throw error
        decrypt_message(tampered_b64)

        end = time.time()
        duration = round((end - start) * 1000, 3)

        return {
            "status": "FAIL",
            "time": duration,
            "details": "Tampered message decrypted (MAC NOT working!)"
        }

    except Exception:
        end = time.time()
        duration = round((end - start) * 1000, 3)

        return {
            "status": "PASS",
            "time": duration,
            "details": "Tampering detected: MAC verification failed"
        }
