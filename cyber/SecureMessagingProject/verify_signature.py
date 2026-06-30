from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

# Load User A's Public Key
with open("keys/userA_public.pem", "rb") as key_file:
    public_key = serialization.load_pem_public_key(
        key_file.read()
    )

# Read Original Message
with open("messages/original_message.txt", "r") as file:
    message = file.read()

# Read Signature
with open("messages/signature.sig", "rb") as file:
    signature = file.read()

# Verify Signature
try:
    public_key.verify(
        signature,
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    print("✅ Signature Verified Successfully!")
    print("Message is Authentic.")

except InvalidSignature:
    print("❌ Signature Verification Failed!")
    print("Message may have been modified.")