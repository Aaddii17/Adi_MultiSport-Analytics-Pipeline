import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ==========================================
# FOOTBALL API ENGINE (LiveScore by Api Dojo)
# ==========================================
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

def parse_livescore_time(time_str):
    """Helper to parse LiveScore's unique YYYYMMDDHHMMSS format."""
    try:
        dt = datetime.strptime(str(time_str)[:14], "%Y%m%d%H%M%S")
        return dt.strftime("%b %d, %I:%M %p")
    except:
        return str(time_str)

def run_live_football():
    st.header("⚽ Live Football Center & Global Schedule")
    st.markdown("---")
    
    if "FOOTBALL_API_KEY" not in st.secrets:
        st.error("API Key missing! Please add 'FOOTBALL_API_KEY' to Streamlit Secrets.")
        return

    if st.button("🔄 Refresh Football Scores"):
        st.cache_data.clear()
        st.rerun()

    tab1, tab2 = st.tabs(["🔴 Live Matches", "📅 Today's Schedule"])

    # ==========================================
    # TAB 1: LIVE MATCHES
    # ==========================================
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
                st.info("No live matches currently being played.")
        else:
            st.info("No live matches currently being played.")

    # ==========================================
    # TAB 2: TODAY'S SCHEDULE
    # ==========================================
    with tab2:
        with st.spinner("Fetching today's fixtures..."):
            today_date = datetime.now().strftime("%Y%m%d")
            upcoming_data = fetch_football_data("matches/v2/list-by-date", params={"Category": "soccer", "Date": today_date})
        
        if upcoming_data and 'Stages' in upcoming_data:
            up_list = []
            for stage in upcoming_data['Stages']:
                league = f"{stage.get('Cnm', '')} - {stage.get('Snm', '')}"
                for match in stage.get('Events', []):
                    # EPS 'NS' means Not Started
                    if match.get('Eps') == 'NS':
                        time_str = match.get('Esd', '')
                        match_time = parse_livescore_time(time_str)
                        up_list.append({
                            "League": league,
                            "Home": match.get('T1', [{}])[0].get('Nm', 'Home'),
                            "Away": match.get('T2', [{}])[0].get('Nm', 'Away'),
                            "Kickoff Time": match_time
                        })
            if up_list:
                st.dataframe(pd.DataFrame(up_list), use_container_width=True, hide_index=True)
            else:
                st.info("No upcoming fixtures found for today.")
        else:
            st.info("No upcoming fixtures found.")