from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# ----------------------------
# AES Encryption Function
# ----------------------------
def encrypt_message(message, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(message.encode())

    return {
        "nonce": base64.b64encode(cipher.nonce).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "tag": base64.b64encode(tag).decode()
    }

# ----------------------------
# AES Decryption Function
# ----------------------------
def decrypt_message(encrypted_data, key):
    nonce = base64.b64decode(encrypted_data["nonce"])
    ciphertext = base64.b64decode(encrypted_data["ciphertext"])
    tag = base64.b64decode(encrypted_data["tag"])

    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    plaintext = cipher.decrypt_and_verify(ciphertext, tag)

    return plaintext.decode()

# ----------------------------
# Generate AES Key (16 bytes = 128-bit)
# ----------------------------
def generate_aes_key():
    return get_random_bytes(16)