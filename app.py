import streamlit as st
import json
import os
from zxcvbn import zxcvbn

PASSWORD_FILE = "passwords.json"

# Function to check password strength
def check_password_strength(password):
    result = zxcvbn(password)
    return result["score"], result["feedback"]

# Function to load saved passwords
def load_passwords():
    if os.path.exists(PASSWORD_FILE):
        with open(PASSWORD_FILE, "r") as file:
            return json.load(file)
    return {}

# Function to save password
def save_password(name, password):
    passwords = load_passwords()
    passwords[name] = password
    with open(PASSWORD_FILE, "w") as file:
        json.dump(passwords, file, indent=4)
    st.success("✅ Password saved successfully!")

# Streamlit UI
st.title("🔒 Password Strength Meter & Saver")

name = st.text_input("Enter a name for the password (e.g., Gmail, Facebook)")
password = st.text_input("Enter your password", type="password")

if password:
    score, feedback = check_password_strength(password)
    strength_levels = ["Very Weak", "Weak", "Medium", "Strong", "Very Strong"]

    st.write(f"**Strength Score:** {score} / 4")
    st.progress((score + 1) / 5)
    st.write(f"**Strength Level:** {strength_levels[score]}")

    if feedback["suggestions"]:
        st.write("💡 **Suggestions:**")
        for suggestion in feedback["suggestions"]:
            st.write(f"- {suggestion}")

    if st.button("Save Password"):
        if name and password:
            save_password(name, password)
        else:
            st.warning("⚠️ Please enter both a name and a password.")

# Show saved passwords
st.subheader("🔐 Saved Passwords")
saved_passwords = load_passwords()
if saved_passwords:
    for site, pwd in saved_passwords.items():
        st.write(f"**{site}:** `{pwd}`")
else:
    st.write("No passwords saved yet.")




