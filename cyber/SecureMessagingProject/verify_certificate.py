import json
import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# -------------------------------------
# Load CA Public Key
# -------------------------------------
with open("certificates/ca_public.pem", "rb") as f:
    ca_public_key = serialization.load_pem_public_key(f.read())


# -------------------------------------
# Function to Verify Certificate
# -------------------------------------
def verify_certificate(username):

    try:

        # Read Certificate
        with open(f"certificates/{username}_cert.json", "r") as f:
            cert = json.load(f)

        certificate = cert["certificate"]

        signature = base64.b64decode(cert["signature"])

        certificate_bytes = json.dumps(
            certificate,
            sort_keys=True
        ).encode()

        # Verify Signature
        ca_public_key.verify(
            signature,
            certificate_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        print(f"{username} Certificate : VALID")

        return True

    except Exception:

        print(f"{username} Certificate : INVALID")

        return False


# -------------------------------------
# Verify Both Users
# -------------------------------------
print("=" * 45)
print(" CERTIFICATE VERIFICATION")
print("=" * 45)

userA = verify_certificate("userA")
userB = verify_certificate("userB")

print("=" * 45)

if userA and userB:
    print("ALL CERTIFICATES ARE TRUSTED")
else:
    print("CERTIFICATE VERIFICATION FAILED")

print("=" * 45)