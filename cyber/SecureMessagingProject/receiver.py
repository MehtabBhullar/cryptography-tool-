from Crypto.Cipher import AES
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import ast

# -------------------------------------
# Load User B Private Key
# -------------------------------------
with open("keys/userB_private.pem", "rb") as f:
    receiver_private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# -------------------------------------
# Load User A Public Key
# -------------------------------------
with open("keys/userA_public.pem", "rb") as f:
    sender_public_key = serialization.load_pem_public_key(f.read())

# -------------------------------------
# Read Encrypted AES Key
# -------------------------------------
with open("messages/encrypted_key.bin", "rb") as f:
    encrypted_aes_key = f.read()

# -------------------------------------
# Read Encrypted Message
# -------------------------------------
with open("messages/encrypted_data.txt", "r") as f:
    encrypted_data = ast.literal_eval(f.read())

# -------------------------------------
# Read Digital Signature
# -------------------------------------
with open("messages/signature.sig", "rb") as f:
    signature = f.read()

# -------------------------------------
# RSA Decrypt AES Key
# -------------------------------------
aes_key = receiver_private_key.decrypt(
    encrypted_aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

# -------------------------------------
# AES Decrypt Message
# -------------------------------------
nonce = base64.b64decode(encrypted_data["nonce"])
ciphertext = base64.b64decode(encrypted_data["ciphertext"])
tag = base64.b64decode(encrypted_data["tag"])

cipher = AES.new(aes_key, AES.MODE_EAX, nonce=nonce)

message = cipher.decrypt_and_verify(ciphertext, tag).decode()

# -------------------------------------
# Create SHA-256 Hash
# -------------------------------------
digest = hashes.Hash(hashes.SHA256())
digest.update(message.encode())
message_hash = digest.finalize()

# -------------------------------------
# Verify Digital Signature
# -------------------------------------
try:
    sender_public_key.verify(
        signature,
        message_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    print("=" * 45)
    print(" MESSAGE RECEIVED SUCCESSFULLY ")
    print("=" * 45)
    print("Original Message : ", message)
    print("Signature Status : VALID")
    print("=" * 45)

except Exception:

    print("=" * 45)
    print(" WARNING ")
    print("=" * 45)
    print("Signature Verification FAILED")
    print("Message may have been tampered!")
    print("=" * 45)