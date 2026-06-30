from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

# Load User A's Private Key
with open("keys/userA_private.pem", "rb") as key_file:
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None
    )

# Message to be signed
message = input("Enter message to sign: ")

# Create Digital Signature
signature = private_key.sign(
    message.encode(),
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

# Save Signature
with open("messages/signature.sig", "wb") as file:
    file.write(signature)

# Save Original Message
with open("messages/original_message.txt", "w") as file:
    file.write(message)

print("✅ Digital Signature Created Successfully!")