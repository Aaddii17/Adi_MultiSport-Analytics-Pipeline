import streamlit as st
import requests

def run_live_football():
    st.header("⚽ Real-Time Live Football")
    st.markdown("---")
    
    # 1. Securely fetch the API key
    api_key = st.secrets.get("FOOTBALL_API_KEY")
    if not api_key:
        st.error("⚠️ API Key is missing. Please check your Streamlit Secrets.")
        return

    # 2. Setup the API-Football endpoint for live matches
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
    }
    params = {"live": "all"}

    # 3. Fetch and display the data
    with st.spinner("Fetching live action..."):
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json().get('response', [])
                
                if not data:
                    st.info("No live professional matches are happening right now.")
                    return

                # Build a simple, clean UI for each match
                for match in data:
                    league = match.get('league', {}).get('name', 'Unknown League')
                    home_team = match.get('teams', {}).get('home', {}).get('name', 'Home')
                    away_team = match.get('teams', {}).get('away', {}).get('name', 'Away')
                    home_goals = match.get('goals', {}).get('home', 0)
                    away_goals = match.get('goals', {}).get('away', 0)
                    elapsed = match.get('fixture', {}).get('status', {}).get('elapsed', 0)

                    st.markdown(f"""
                    <div style='background-color: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 12px; border-left: 5px solid #00B4D8;'>
                        <small style='color: #00B4D8; font-weight: bold; text-transform: uppercase;'>{league}</small><br>
                        <h4 style='margin: 5px 0; color: white;'>{home_team} {home_goals} - {away_goals} {away_team}</h4>
                        <span style='color: #ff4b4b;'>⏱️ {elapsed}'</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.error(f"API Error: {response.status_code}. Please check your RapidAPI limits.")
                
        except Exception as e:
            st.error("Connection failed. Please try refreshing.")