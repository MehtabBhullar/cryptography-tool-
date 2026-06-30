from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import os

# Create 'keys' folder if it doesn't exist
os.makedirs("keys", exist_ok=True)

def generate_keys(username):
    # Generate Private Key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    # Generate Public Key
    public_key = private_key.public_key()

    # Save Private Key
    with open(f"keys/{username}_private.pem", "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Save Public Key
    with open(f"keys/{username}_public.pem", "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print(f" Keys generated successfully for {username}")

# Generate keys for both users
generate_keys("userA")
generate_keys("userB")

print("\n All RSA keys generated successfully!")