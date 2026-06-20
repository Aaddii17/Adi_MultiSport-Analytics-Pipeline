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
        elif response.status_code == 429:
            st.sidebar.error("⚠️ Football Quota Limit Reached.")
            return None
        elif response.status_code == 403:
            st.sidebar.error("❌ Football API Key Invalid or Missing.")
            return None
        else:
            st.sidebar.error(f"⚠️ API Error: {response.status_code}")
            return None
    except Exception:
        st.sidebar.error("🚨 Connection Timeout.")
        return None

def format_football_date(date_int):
    if not date_int:
        return "TBD"
    try:
        # LiveScore often returns YYYYMMDD format
        date_str = str(date_int)
        dt = datetime.strptime(date_str, "%Y%m%d")
        return dt.strftime("%b %d, %Y")
    except Exception:
        return str(date_int)

def run_live_football():
    st.header("⚽ Live Football Center & Global Schedule")
    st.markdown("---")
    
    if "FOOTBALL_API_KEY" not in st.secrets:
        st.error("API Key missing! Please add 'FOOTBALL_API_KEY' to Streamlit Secrets.")
        return

    if st.button("🔄 Refresh Football Scores"):
        st.cache_data.clear() # Force fetch new data
        st.rerun()

    tab1, tab2 = st.tabs(["🔴 Live Matches", "📅 Upcoming Fixtures"])

    # ==========================================
    # TAB 1: LIVE MATCH TRACKER
    # ==========================================
    with tab1:
        with st.spinner("Fetching live football action..."):
            # LiveScore API uses category 'soccer'
            live_data = fetch_football_data("matches/v2/list-live", params={"Category": "soccer"})
            
        if live_data and 'Stages' in live_data:
            live_found = False
            for stage in live_data['Stages']:
                league_name = stage.get('Snm', 'Unknown League')
                country = stage.get('Cnm', '')
                
                for match in stage.get('Events', []):
                    live_found = True
                    home_team = match.get('T1', [{}])[0].get('Nm', 'Home')
                    away_team = match.get('T2', [{}])[0].get('Nm', 'Away')
                    
                    home_goals = match.get('Tr1', '0')
                    away_goals = match.get('Tr2', '0')
                    
                    elapsed_time = match.get('Eps', 'Live')

                    st.markdown(f"""
                    <div style='background-color: #111; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #00B4D8; box-shadow: 0 4px 6px rgba(0,0,0,0.3);'>
                        <span style='color: #00B4D8; font-weight: bold; font-size: 12px; text-transform: uppercase;'>🌍 {country} - {league_name}</span>
                        <h3 style='margin: 10px 0 5px 0; color: white;'>
                            {home_team} <span style='color: #00B4D8; font-size: 24px;'>{home_goals}</span>
                            <span style='color: gray; font-size: 16px; margin: 0 15px;'>vs</span> 
                            {away_team} <span style='color: #00B4D8; font-size: 24px;'>{away_goals}</span>
                        </h3>
                        <p style='color: #FF4B4B; margin: 0; font-size: 14px; font-weight: 500;'>⏱️ {elapsed_time}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
            if not live_found:
                st.info("No professional football matches are currently being played. Check the upcoming schedule!")
        else:
            st.info("No professional football matches are currently being played. Check the upcoming schedule!")

    # ==========================================
    # TAB 2: UPCOMING FIXTURES
    # ==========================================
    with tab2:
        with st.spinner("Compiling today's global fixtures..."):
            # LiveScore API requires a date format YYYYMMDD
            today_date = datetime.now().strftime("%Y%m%d")
            upcoming_data = fetch_football_data("matches/v2/list-by-date", params={"Category": "soccer", "Date": today_date})
            
        if upcoming_data and 'Stages' in upcoming_data:
            up_list = []
            for stage in upcoming_data['Stages']:
                league = stage.get('Snm', '')
                for match in stage.get('Events', []):
                    # Only add matches that haven't started yet
                    if match.get('Eps') == 'NS': 
                        # Try to construct a time string if available, otherwise just use the date
                        match_time = str(match.get('Esd', ''))
                        if len(match_time) >= 14:
                            try:
                                dt = datetime.strptime(match_time[:14], "%Y%m%d%H%M%S")
                                time_str = dt.strftime("%I:%M %p")
                            except:
                                time_str = "TBD"
                        else:
                            time_str = "TBD"
                            
                        up_list.append({
                            "League": league,
                            "Home Team": match.get('T1', [{}])[0].get('Nm', ''),
                            "Away Team": match.get('T2', [{}])[0].get('Nm', ''),
                            "Time": time_str
                        })
            if up_list:
                st.dataframe(pd.DataFrame(up_list), use_container_width=True, hide_index=True)
            else:
                st.info("No upcoming fixtures found for today.")
        else:
            st.info("No upcoming fixtures found.")