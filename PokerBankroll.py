import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import io

st.set_page_config(page_title="Poker Bankroll Tracker", page_icon="🃏")
st.title("🎲 Poker Bankroll Tracker")
st.markdown("Track your poker sessions, view your bankroll growth, and gain insights from your play.")

# Session storage (for MVP)
if "session_data" not in st.session_state:
    st.session_state.session_data = []

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
        st.session_state.session_data.append({
            "Date": date,
            "Game Type": game_type,
            "Location": location,
            "Buy-In": buy_in,
            "Cash-Out": cash_out,
            "Profit": profit,
            "Hours": hours,
            "Hourly Rate": hourly_rate,
            "Notes": notes
        })
        st.success("Session added successfully!")

# --- Data Display ---
st.header("📋 Session History")
df = pd.DataFrame(st.session_state.session_data)
if not df.empty:
    df_sorted = df.sort_values("Date")
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
    buffer = io.StringIO()
    df.to_csv(buffer, index=False)
    st.download_button("Download CSV", data=buffer.getvalue(), file_name="poker_sessions.csv", mime="text/csv")

else:
    st.info("No session data yet. Add a session to get started!")




