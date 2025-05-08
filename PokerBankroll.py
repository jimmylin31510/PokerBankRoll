import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pyrebase4

# Firebase Configuration
firebase_config = {
    "apiKey": "AIzaSyBFOO1L0pZkmI973GA4z6CIw2Bv3nnJ8sc",
    "authDomain": "pokerbankroll-cba0e.firebaseapp.com",
    "projectId": "pokerbankroll-cba0e",
    "storageBucket": "pokerbankroll-cba0e.firebasestorage.app",
    "messagingSenderId": "774301975832",
    "appId": "1:774301975832:web:c0205662c4b2bb076e0a6d",
    "databaseURL": ""
}

firebase = pyrebase4.initialize_app(firebase_config)
auth = firebase.auth()
db = firebase.database()

# App title
st.set_page_config(page_title="Poker Bankroll Tracker", page_icon="🃏")
st.title("🎲 Poker Bankroll Tracker")

# Session state for login
if "user" not in st.session_state:
    st.session_state.user = None

# Authentication UI
def login():
    st.subheader("🔐 Login or Sign Up")
    choice = st.radio("Login or Sign Up", ["Login", "Sign Up"])
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Submit"):
        try:
            if choice == "Login":
                user = auth.sign_in_with_email_and_password(email, password)
            else:
                user = auth.create_user_with_email_and_password(email, password)
            st.session_state.user = user
            st.success("Successfully logged in!")
        except Exception as e:
            st.error(f"Authentication failed: {e}")

if not st.session_state.user:
    login()
    st.stop()

user_id = st.session_state.user["localId"]
session_ref = f"users/{user_id}/sessions"

# Load user's session data from Firebase
session_data = db.child(session_ref).get().val()
if not session_data:
    session_data = {}

# --- Input Form ---
st.header("Add New Session")
with st.form("session_form"):
    col1, col2 = st.columns(2)
    with col1:
        date = st.date_input("Date", value=datetime.date.today())
        game_type = st.selectbox("Game Type", ["Cash", "Tournament", "Online", "Live"])
        location = st.text_input("Location / Platform", "")
    with col2:
        buy_in = st.number_input("Buy-In ($)", min_value=0.0, step=1.0)
        cash_out = st.number_input("Cash Out ($)", min_value=0.0, step=1.0)
        hours = st.number_input("Session Duration (Hours)", min_value=0.0, step=0.1)
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Add Session")

    if submitted:
        profit = cash_out - buy_in
        hourly_rate = profit / hours if hours > 0 else 0
        entry = {
            "Date": str(date),
            "Game Type": game_type,
            "Location": location,
            "Buy-In": buy_in,
            "Cash-Out": cash_out,
            "Profit": profit,
            "Hours": hours,
            "Hourly Rate": hourly_rate,
            "Notes": notes
        }
        db.child(session_ref).push(entry)
        st.success("Session added successfully! Please refresh to see updated data.")

# Convert session data to DataFrame
records = list(session_data.values()) if session_data else []
df = pd.DataFrame(records)
if not df.empty:
    df["Date"] = pd.to_datetime(df["Date"])
    df_sorted = df.sort_values("Date")
    st.header("📋 Session History")
    st.dataframe(df_sorted, use_container_width=True)

    # --- Stats ---
    st.subheader("📊 Summary Statistics")
    total_sessions = len(df)
    total_profit = df["Profit"].sum()
    avg_hourly = df["Hourly Rate"].mean()
    total_hours = df["Hours"].sum()

    st.markdown(f"- **Total Sessions:** {total_sessions}")
    st.markdown(f"- **Total Profit:** ${total_profit:.2f}")
    st.markdown(f"- **Total Hours Played:** {total_hours:.1f} hrs")
    st.markdown(f"- **Average Hourly Rate:** ${avg_hourly:.2f}/hr")

    # --- Charts ---
    st.subheader("📈 Bankroll Over Time")
    df_sorted["Cumulative Profit"] = df_sorted["Profit"].cumsum()
    st.line_chart(df_sorted.set_index("Date")["Cumulative Profit"])

    st.subheader("🎯 Profit by Game Type")
    game_group = df.groupby("Game Type")["Profit"].sum()
    st.bar_chart(game_group)

    # --- Export CSV ---
    st.subheader("⬇️ Export Data")
    csv = df.to_csv(index=False)
    st.download_button("Download CSV", data=csv, file_name="poker_sessions.csv", mime="text/csv")
else:
    st.info("No session data yet. Add a session to get started!")
