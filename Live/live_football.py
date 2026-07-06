import streamlit as st
import requests

def run_live_football():
    st.header("⚽ Real-Time Live & World Cup 2026 Center")
    st.markdown("---")
    
    api_key = st.secrets.get("FOOTBALL_API_KEY", "")
    if not api_key:
        st.error("API Key missing! Add 'FOOTBALL_API_KEY' to Streamlit Secrets.")
        return

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }

    # Create tabs to separate live matches from the World Cup schedule
    tab1, tab2 = st.tabs(["🔴 Live Right Now", "🏆 FIFA World Cup 2026"])

    # ==========================================
    # TAB 1: STRICTLY LIVE MATCHES
    # ==========================================
    with tab1:
        st.subheader("Currently Playing")
        with st.spinner("Checking stadiums..."):
            try:
                response = requests.get("https://api-football-v1.p.rapidapi.com/v3/fixtures", headers=headers, params={"live": "all"}, timeout=10)
                if response.status_code == 200:
                    data = response.json().get('response', [])
                    if not data:
                        st.info("No professional matches are being played at this exact moment. Check the World Cup tab!")
                    else:
                        for match in data:
                            league = match.get('league', {}).get('name', 'Unknown')
                            home = match.get('teams', {}).get('home', {}).get('name', 'Home')
                            away = match.get('teams', {}).get('away', {}).get('name', 'Away')
                            home_goals = match.get('goals', {}).get('home', 0)
                            away_goals = match.get('goals', {}).get('away', 0)
                            elapsed = match.get('fixture', {}).get('status', {}).get('elapsed', 0)

                            st.markdown(f"""
                            <div style='background-color: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 12px; border-left: 5px solid #00B4D8;'>
                                <small style='color: #00B4D8; font-weight: bold; text-transform: uppercase;'>{league}</small><br>
                                <h4 style='margin: 5px 0; color: white;'>{home} {home_goals} - {away_goals} {away}</h4>
                                <span style='color: #ff4b4b;'>⏱️ {elapsed}'</span>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception:
                st.error("Connection failed.")

    # ==========================================
    # TAB 2: FIFA WORLD CUP 2026
    # ==========================================
    with tab2:
        st.subheader("World Cup 2026 Fixtures & Results")
        # League ID 1 is the FIFA World Cup in API-Football
        params = {"league": "1", "season": "2026"}
        with st.spinner("Loading World Cup data..."):
            try:
                response = requests.get("https://api-football-v1.p.rapidapi.com/v3/fixtures", headers=headers, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json().get('response', [])
                    if not data:
                        st.warning("World Cup 2026 data is currently syncing with the provider.")
                    else:
                        # Displaying the most relevant matches
                        for match in data[:15]: 
                            date = match.get('fixture', {}).get('date', '').split('T')[0]
                            home = match.get('teams', {}).get('home', {}).get('name', 'Home')
                            away = match.get('teams', {}).get('away', {}).get('name', 'Away')
                            status = match.get('fixture', {}).get('status', {}).get('long', '')
                            home_goals = match.get('goals', {}).get('home')
                            away_goals = match.get('goals', {}).get('away')
                            
                            score_str = f"{home_goals} - {away_goals}" if home_goals is not None else "vs"

                            st.markdown(f"""
                            <div style='background-color: #2b2b2b; padding: 10px; border-radius: 5px; margin-bottom: 8px; border-left: 3px solid #f1c40f;'>
                                <small style='color: #bdc3c7;'>📅 {date} | {status}</small><br>
                                <b style='color: white;'>{home} {score_str} {away}</b>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception:
                st.error("Connection failed.")