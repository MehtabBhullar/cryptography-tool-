import os
import json
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# -------------------------------------
# Create certificates folder
# -------------------------------------
os.makedirs("certificates", exist_ok=True)

# -------------------------------------
# Generate CA RSA Key Pair
# -------------------------------------
ca_private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

ca_public_key = ca_private_key.public_key()

# -------------------------------------
# Save CA Private Key
# -------------------------------------
with open("certificates/ca_private.pem", "wb") as f:
    f.write(
        ca_private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

# -------------------------------------
# Save CA Public Key
# -------------------------------------
with open("certificates/ca_public.pem", "wb") as f:
    f.write(
        ca_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("CA Keys Generated Successfully")

# -------------------------------------
# Function to Create Certificate
# -------------------------------------
def create_certificate(username):

    # Load user's public key
    with open(f"keys/{username}_public.pem", "rb") as f:
        user_public_key = f.read()

    # Certificate Data
    certificate = {
        "owner": username,
        "public_key": base64.b64encode(user_public_key).decode()
    }

    certificate_bytes = json.dumps(
        certificate,
        sort_keys=True
    ).encode()

    # Create Digital Signature
    signature = ca_private_key.sign(
        certificate_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    final_certificate = {
        "certificate": certificate,
        "signature": base64.b64encode(signature).decode()
    }

    # Save Certificate
    with open(f"certificates/{username}_cert.json", "w") as f:
        json.dump(final_certificate, f, indent=4)

    print(f"Certificate Issued for {username}")


# -------------------------------------
# Generate Certificates
# -------------------------------------
create_certificate("userA")
create_certificate("userB")

print("\n===================================")
print(" MINI PKI CREATED SUCCESSFULLY ")
print("===================================")
print("Generated:")
print("ca_private.pem")
print("ca_public.pem")
print("userA_cert.json")
print("userB_cert.json")
print("===================================")