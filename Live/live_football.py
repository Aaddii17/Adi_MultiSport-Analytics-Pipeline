import streamlit as st
import requests
import pandas as pd
from datetime import datetime

@st.cache_data(ttl=90)
def fetch_football_data(endpoint, params=None):
    """Fetches data from LiveScore API with a 90-second cache."""
    api_key = st.secrets.get("FOOTBALL_API_KEY", "")
    api_host = "livescore6.p.rapidapi.com"
    
    url = f"https://{api_host}/{endpoint}"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def run_live_football():
    st.header("⚽ Live Football Center & Global Schedule")
    st.markdown("---")
    
    if "FOOTBALL_API_KEY" not in st.secrets:
        st.error("API Key missing! Please add 'FOOTBALL_API_KEY' to Streamlit Secrets.")
        return

    if st.button("🔄 Refresh Football Scores"):
        st.cache_data.clear()
        st.rerun()

    tab1, tab2 = st.tabs(["🔴 Live Matches", "📅 Upcoming Fixtures"])

    with tab1:
        with st.spinner("Fetching live football action..."):
            live_data = fetch_football_data("matches/v2/list-live", params={"Category": "soccer"})
            
        if live_data and 'Stages' in live_data:
            live_found = False
            for stage in live_data['Stages']:
                country = stage.get('Cnm', '')
                league_name = stage.get('Snm', '')
                
                for match in stage.get('Events', []):
                    live_found = True
                    home_team = match.get('T1', [{}])[0].get('Nm', 'Home')
                    away_team = match.get('T2', [{}])[0].get('Nm', 'Away')
                    home_goals = match.get('Tr1', '0')
                    away_goals = match.get('Tr2', '0')
                    elapsed_time = match.get('Eps', 'Live')

                    st.markdown(f"""
                    <div style='background-color: #111; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 4px solid #00B4D8;'>
                        <small style='color: #00B4D8;'>{country} - {league_name}</small>
                        <h4 style='color: white;'>{home_team} {home_goals} vs {away_goals} {away_team}</h4>
                        <p style='color: #FF4B4B;'>⏱️ {elapsed_time}</p>
                    </div>
                    """, unsafe_allow_html=True)
            if not live_found:
                st.info("No live matches currently.")
        else:
            st.info("No live matches currently.")

    with tab2:
        st.write("Upcoming fixtures list initialized.")