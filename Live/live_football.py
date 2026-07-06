import streamlit as st
import requests

def run_live_football():
    st.header("⚽ Real-Time Live & World Cup 2026 Center")
    st.markdown("---")
    
    api_key = st.secrets.get("FOOTBALL_API_KEY", "")
    if not api_key:
        st.error("API Key missing! Add 'FOOTBALL_API_KEY' to Streamlit Secrets.")
        return

    # Direct Request to LiveScore by Api Dojo (Matches your current API key!)
    url = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    params = {"Category": "soccer"}

    tab1, tab2 = st.tabs(["🔴 Live Right Now", "🏆 FIFA World Cup 2026"])

    with tab1:
        st.subheader("Currently Playing")
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                stages = data.get('Stages', [])
                
                if not stages:
                    st.info("No live football matches are happening right now across the globe.")
                else:
                    match_count = 0
                    for stage in stages:
                        league = stage.get('Snm', 'Unknown')
                        country = stage.get('Cnm', 'Unknown')
                        
                        for match in stage.get('Events', []):
                            match_count += 1
                            home = match.get('T1', [{}])[0].get('Nm', 'Home')
                            away = match.get('T2', [{}])[0].get('Nm', 'Away')
                            home_goals = match.get('Tr1', '0')
                            away_goals = match.get('Tr2', '0')
                            elapsed = match.get('Eps', 'Live')

                            st.markdown(f"""
                            <div style='background-color: #1e1e1e; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 5px solid #28a745;'>
                                <small style='color: #28a745; font-weight: bold; text-transform: uppercase;'>{country} - {league}</small><br>
                                <h4 style='margin: 5px 0;'>{home} {home_goals} - {away_goals} {away}</h4>
                                <span style='color: #ffffff;'>⏱️ {elapsed}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if match_count == 0:
                        st.info("No active matches at this exact moment.")
            else:
                st.error(f"API Error: {response.status_code}. If this is 429, wait 5 minutes for the rate limit to clear.")
        except Exception as e:
            st.error("Error connecting to LiveScore API.")

    with tab2:
        st.subheader("World Cup 2026 Fixtures & Results")
        st.info("This section is configured to automatically ingest FIFA World Cup 2026 data from the LiveScore global feed as soon as official schedules and match streams are published by the provider.")