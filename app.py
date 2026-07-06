import streamlit as st
from live_football import run_live_football

st.set_page_config(page_title="Sports Analytics Pipeline", layout="wide")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to:", ["Home", "Live Football"])

if page == "Home":
    st.title("🏆 Multi-Sport Analytics")
    st.write("Welcome to the main dashboard. Select an option from the sidebar.")
elif page == "Live Football":
    run_live_football()