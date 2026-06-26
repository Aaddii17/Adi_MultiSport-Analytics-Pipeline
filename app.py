import streamlit as st
from Live.live_cricket import run_live_cricket
from Live.live_football import run_live_football

# If you have historical analytics files, import them here later!
# from History.cricket_history import run_cricket_history 

st.set_page_config(page_title="AdiSports Pipeline", layout="wide")

with st.sidebar:
    st.title("Navigation")
    sport = st.radio("Select Sport", ["Cricket", "Football", "Real-Time Live Center"])
    
    stream = None
    if sport == "Real-Time Live Center":
        stream = st.selectbox("Select Live Stream", ["Live Cricket Tracking", "Live Football Tracker"])

# ==========================================
# CORRECTED ROUTING LOGIC
# ==========================================
if sport == "Cricket":
    st.title("🏏 Cricket Historical Analytics")
    st.info("Your historical cricket data and visualizations go here. To see live matches, select 'Real-Time Live Center' from the sidebar!")
    # run_cricket_history() 

elif sport == "Football":
    st.title("⚽ Football Historical Analytics")
    st.info("Your historical football data and visualizations go here. To see live matches, select 'Real-Time Live Center' from the sidebar!")
    # run_football_history()

elif sport == "Real-Time Live Center":
    if stream == "Live Cricket Tracking":
        run_live_cricket()
    elif stream == "Live Football Tracker":
        run_live_football()