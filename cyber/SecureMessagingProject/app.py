
import streamlit as st
import subprocess

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="Secure Messaging System",
    page_icon="🔐",
    layout="wide"
)

# ----------------------------------------
# Header
# ----------------------------------------
st.title("🔐 Secure Messaging System")
st.markdown("### AES-128 | RSA-2048 | Digital Signature | Mini PKI")

st.divider()

# ----------------------------------------
# Tabs
# ----------------------------------------
tab1, tab2, tab3 = st.tabs(
    [
        "📤 Sender",
        "📥 Receiver",
        "🏢 PKI Verification"
    ]
)

# ===================================================
# SENDER
# ===================================================
with tab1:

    st.header("📤 Sender Panel")

    message = st.text_area(
        "Enter Message",
        placeholder="Type your message here...",
        height=180
    )

    if st.button("🔒 Encrypt & Send"):

        if message.strip() == "":
            st.warning("Please enter a message.")

        else:

            with st.spinner("Encrypting Message..."):

                result = subprocess.run(
                    ["python", "sender.py", message],
                    capture_output=True,
                    text=True
                )

            if result.returncode == 0:

                st.success("Message Sent Successfully")

                st.code(result.stdout)

            else:

                st.error("Encryption Failed")

                st.code(result.stderr)

# ===================================================
# RECEIVER
# ===================================================
with tab2:

    st.header("📥 Receiver Panel")

    st.write("Decrypt encrypted files and verify signature.")

    if st.button("📥 Decrypt & Verify"):

        with st.spinner("Decrypting..."):

            result = subprocess.run(
                ["python", "receiver.py"],
                capture_output=True,
                text=True
            )

        if result.returncode == 0:

            st.success("Receiver Process Completed")

            st.code(result.stdout)

            if "VALID" in result.stdout:

                st.success("Digital Signature Verified ✅")

            else:

                st.error("Signature Verification Failed ❌")

        else:

            st.error("Receiver Error")

            st.code(result.stderr)

# ===================================================
# PKI
# ===================================================
with tab3:

    st.header("🏢 PKI Verification")

    st.write("Verify certificates issued by the Certificate Authority.")

    col1, col2 = st.columns(2)

    with col1:

        if st.button("⚙ Generate Certificates"):

            with st.spinner("Generating Certificates..."):

                result = subprocess.run(
                    ["python", "certificate_authority.py"],
                    capture_output=True,
                    text=True
                )

            if result.returncode == 0:

                st.success("Certificates Generated")

                st.code(result.stdout)

            else:

                st.error("Generation Failed")

                st.code(result.stderr)

    with col2:

        if st.button("✔ Verify Certificates"):

            with st.spinner("Verifying..."):

                result = subprocess.run(
                    ["python", "verify_certificate.py"],
                    capture_output=True,
                    text=True
                )

            if result.returncode == 0:

                st.code(result.stdout)

                if "TRUSTED" in result.stdout:

                    st.success("All Certificates Trusted ✅")

                else:

                    st.error("Certificate Verification Failed")

            else:

                st.error("Verification Error")

                st.code(result.stderr)

st.divider()

st.caption("ESS Project | Secure Messaging using Hybrid Cryptography")

