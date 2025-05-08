import streamlit as st
import pyrebase
import time

# Firebase Configuration
firebase_config = {
    "apiKey": "AIzaSyBFOO1L0pZkmI973GA4z6CIw2Bv3nnJ8sc",
    "authDomain": "pokerbankroll-cba0e.firebaseapp.com",
    "projectId": "pokerbankroll-cba0e",
    "storageBucket": "pokerbankroll-cba0e.firebasestorage.app",
    "messagingSenderId": "774301975832",
    "appId": "1:774301975832:web:c0205662c4b2bb076e0a6d",
    "databaseURL": "https://pokerbankroll-cba0e-default-rtdb.firebaseio.com/"
}

firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

st.set_page_config(page_title="Login | Poker Tracker", page_icon="🔐")
st.title("🔐 Login or Sign Up")

# 清除登入狀態（選擇性）
if "user" not in st.session_state:
    st.session_state.user = None

choice = st.radio("Select Mode", ["Login", "Sign Up"])
email = st.text_input("Email")
password = st.text_input("Password", type="password")

if st.button("Submit"):
    try:
        if choice == "Login":
            user = auth.sign_in_with_email_and_password(email, password)
        else:
            user = auth.create_user_with_email_and_password(email, password)

        st.session_state.user = user
        st.success("✅ Login successful! Redirecting to main app...")
        time.sleep(1)
        st.switch_page("2_Main.py")

    except Exception as e:
        st.error(f"❌ Authentication failed: {e}")
