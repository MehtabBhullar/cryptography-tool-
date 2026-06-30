from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import base64
import os
import sys

# -------------------------------------
# Create messages folder if not present
# -------------------------------------
os.makedirs("messages", exist_ok=True)

# -------------------------------------
# Load User B Public Key (for RSA Encryption)
# -------------------------------------
with open("keys/userB_public.pem", "rb") as f:
    receiver_public_key = serialization.load_pem_public_key(f.read())

# -------------------------------------
# Load User A Private Key (for Digital Signature)
# -------------------------------------
with open("keys/userA_private.pem", "rb") as f:
    sender_private_key = serialization.load_pem_private_key(
        f.read(),
        password=None
    )

# -------------------------------------
# Get Message
# If message comes from Streamlit, it will be passed as an argument.
# Otherwise ask from terminal.
# -------------------------------------
if len(sys.argv) > 1:
    message = sys.argv[1]
else:
    message = input("Enter your message: ")

# -------------------------------------
# Generate AES Key (128-bit)
# -------------------------------------
aes_key = get_random_bytes(16)

# -------------------------------------
# Encrypt Message using AES (EAX Mode)
# -------------------------------------
cipher = AES.new(aes_key, AES.MODE_EAX)

ciphertext, tag = cipher.encrypt_and_digest(message.encode())

encrypted_data = {
    "nonce": base64.b64encode(cipher.nonce).decode(),
    "ciphertext": base64.b64encode(ciphertext).decode(),
    "tag": base64.b64encode(tag).decode()
}

# Save encrypted message
with open("messages/encrypted_data.txt", "w") as f:
    f.write(str(encrypted_data))

# -------------------------------------
# Encrypt AES Key using Receiver's RSA Public Key
# -------------------------------------
encrypted_aes_key = receiver_public_key.encrypt(
    aes_key,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open("messages/encrypted_key.bin", "wb") as f:
    f.write(encrypted_aes_key)

# -------------------------------------
# Create SHA-256 Hash
# -------------------------------------
digest = hashes.Hash(hashes.SHA256())
digest.update(message.encode())
message_hash = digest.finalize()

# -------------------------------------
# Create Digital Signature
# -------------------------------------
signature = sender_private_key.sign(
    message_hash,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

with open("messages/signature.sig", "wb") as f:
    f.write(signature)

# -------------------------------------
# Success Output
# -------------------------------------
print("=" * 45)
print(" SECURE MESSAGE SENT SUCCESSFULLY ")
print("=" * 45)
print("AES Message Encryption       : SUCCESS")
print("RSA Key Encryption           : SUCCESS")
print("Digital Signature Created    : SUCCESS")
print()
print("Generated Files:")
print(" - encrypted_data.txt")
print(" - encrypted_key.bin")
print(" - signature.sig")
print("=" * 45)