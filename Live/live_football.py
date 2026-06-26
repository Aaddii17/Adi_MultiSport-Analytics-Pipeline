import streamlit as st
import requests
import pandas as pd

# ==========================================
# FOOTBALL API ENGINE (LiveScore by Api Dojo)
# ==========================================
@st.cache_data(ttl=300)
def fetch_football_data(endpoint, params=None):
    """Fetches data from LiveScore API with a 300-second cache."""
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
    except Exception as e:
        return None

def run_live_football():
    st.header("⚽ Real-Time Live Football")
    
    if "FOOTBALL_API_KEY" not in st.secrets:
        st.error("API Key missing! Add 'FOOTBALL_API_KEY' to Streamlit Secrets.")
        return

    # Use 'matches/v2/list-live' to get current games
    with st.spinner("Fetching live football..."):
        data = fetch_football_data("matches/v2/list-live", params={"Category": "soccer"})
    
    if data and 'Stages' in data:
        live_found = False
        for stage in data['Stages']:
            country = stage.get('Cnm', '')
            league_name = stage.get('Snm', '')
            
            for match in stage.get('Events', []):
                live_found = True
                home = match.get('T1', [{}])[0].get('Nm', 'Home')
                away = match.get('T2', [{}])[0].get('Nm', 'Away')
                home_goals = match.get('Tr1', '0')
                away_goals = match.get('Tr2', '0')
                time = match.get('Eps', 'Live')

                st.markdown(f"""
                <div style='background-color: #222; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #00B4D8;'>
                    <b style='color: #00B4D8;'>{country} | {league_name}</b><br>
                    <h4 style='margin: 5px 0;'>{home} {home_goals} - {away_goals} {away}</h4>
                    <span style='color: #FF4B4B;'>⏱️ {time}</span>
                </div>
                """, unsafe_allow_html=True)
        
        if not live_found:
            st.info("No live football matches currently in progress.")
    else:
        st.warning("Could not retrieve live data. Please check your API key/limit.")