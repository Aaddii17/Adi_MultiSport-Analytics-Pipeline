import streamlit as st
from Live.live_cricket import run_live_cricket
from Live.live_football import run_live_football

st.set_page_config(page_title="AdiSports Pipeline", layout="wide")

with st.sidebar:
    st.title("Navigation")
    sport = st.radio("Select Sport", ["Cricket", "Football", "Real-Time Live Center"])
    
    stream = None
    if sport == "Real-Time Live Center":
        stream = st.selectbox("Select Live Stream", ["Live Cricket Tracking", "Live Football Tracker"])

if sport == "Cricket":
    run_live_cricket()
elif sport == "Football":
    run_live_football()
elif sport == "Real-Time Live Center":
    if stream == "Live Cricket Tracking":
        run_live_cricket()
    elif stream == "Live Football Tracker":
        run_live_football()