# auth.py

import streamlit as st
import hashlib

# Dummy user credentials (replace with real DB or hashed auth system in production)
USERS = {
    "user@example.com": hashlib.sha256("password123".encode()).hexdigest(),
    "demo@nutrition.ai": hashlib.sha256("demo123".encode()).hexdigest(),
}

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(email, password):
    """Login UI widget and session handling."""
    hashed_pwd = hash_password(password)        
    if email in USERS and USERS[email] == hashed_pwd:
        st.session_state["user"] = email
        st.success(f"Logged in as {email}")
        st.rerun()
    else:
        st.error("Invalid credentials")

def logout():
    """Logout the current user."""
    if st.sidebar.button("🚪 Logout"):
        if "user" in st.session_state:
            del st.session_state["user"]
        st.success("Logged out.")
        st.rerun()

def get_logged_in_user():
    """Return currently logged in user email or None."""
    return st.session_state.get("user", None)
