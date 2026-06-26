import streamlit as st
import requests

def run_live_football():
    st.header("⚽ Real-Time Live Football")
    
    # We will use a reliable, simple request structure
    api_key = st.secrets.get("FOOTBALL_API_KEY", "")
    
    if not api_key:
        st.error("API Key missing! Add 'FOOTBALL_API_KEY' to Streamlit Secrets.")
        return

    # Using the standard API-Football v3 endpoint
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    # Fetch live matches
    params = {"live": "all"}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json().get('response', [])
            
            if not data:
                st.info("No live matches currently in progress.")
                return

            for match in data:
                league = match.get('league', {}).get('name', 'League')
                home = match.get('teams', {}).get('home', {}).get('name', 'Home')
                away = match.get('teams', {}).get('away', {}).get('name', 'Away')
                goals_home = match.get('goals', {}).get('home', 0)
                goals_away = match.get('goals', {}).get('away', 0)
                elapsed = match.get('fixture', {}).get('status', {}).get('elapsed', 0)

                st.markdown(f"""
                <div style='background-color: #1e1e1e; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #28a745;'>
                    <b style='color: #28a745;'>{league}</b><br>
                    <h4 style='margin: 5px 0;'>{home} {goals_home} - {goals_away} {away}</h4>
                    <span style='color: #ffffff;'>⏱️ {elapsed}'</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.warning(f"API Error: Received status code {response.status_code}. Check your API quota.")
    except Exception as e:
        st.error("Could not fetch data. Ensure your API Key is valid for 'API-Football' on RapidAPI.")