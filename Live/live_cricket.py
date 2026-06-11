import streamlit as st
import requests
import pandas as pd

def fetch_live_matches(api_key):
    """Fetches a list of ongoing and upcoming matches from the Cricbuzz API."""
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error: Received status code {response.status_code}")
            return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

def run_live_cricket():
    st.header("🔴 Live Match Center & Schedule")
    st.markdown("---")
    
    # Securely retrieve the key from the cloud secrets vault (or fall back to local testing)
    if "CRICBUZZ_API_KEY" in st.secrets:
        API_KEY = st.secrets["CRICBUZZ_API_KEY"]
    else:
        st.warning("API Key not found in Streamlit Secrets. Please check your cloud vault setup.")
        return

    # Add a clean refresh button to let users update scores on demand
    if st.button("🔄 Refresh Live Scores"):
        st.rerun()

    with st.spinner("Fetching real-time streams from Cricbuzz..."):
        data = fetch_live_matches(API_KEY)

    if not data or 'typeMatches' not in data:
        st.info("No active matches found at the moment. Check back during match hours!")
        return

    tab1, tab2 = st.tabs(["🔴 Live Match Tracker", "📅 Upcoming Fixtures"])

    # ==========================================
    # TAB 1: LIVE MATCH TRACKER
    # ==========================================
    with tab1:
        live_found = False
        for match_type in data['typeMatches']:
            category_name = match_type.get('matchFormat', 'Other Matches')
            
            for match_wrapper in match_type.get('seriesMatches', []):
                series_name = match_wrapper.get('seriesAdWrapper', {}).get('seriesName', 'International Tour')
                
                for match in match_wrapper.get('seriesMatches', {}).get('matches', []):
                    match_info = match.get('matchInfo', {})
                    match_state = match_info.get('state', '').lower()
                    
                    # Filter for active matches only
                    if match_state in ['live', 'inprogress']:
                        live_found = True
                        status_text = match_info.get('status', 'Match underway')
                        team1 = match_info.get('team1', {}).get('teamName', 'Team A')
                        team2 = match_info.get('team2', {}).get('teamName', 'Team B')
                        
                        # Score extractions
                        match_score = match.get('matchScore', {})
                        t1_score = match_score.get('team1Score', {}).get('inngs1', {}).get('score', '')
                        t1_wkts = match_score.get('team1Score', {}).get('inngs1', {}).get('wickets', 0)
                        t1_overs = match_score.get('team1Score', {}).get('inngs1', {}).get('overs', 0.0)
                        
                        t2_score = match_score.get('team2Score', {}).get('inngs1', {}).get('score', '')
                        t2_wkts = match_score.get('team2Score', {}).get('inngs1', {}).get('wickets', 0)
                        t2_overs = match_score.get('team2Score', {}).get('inngs1', {}).get('overs', 0.0)

                        # Render scoreboard layout
                        st.markdown(f"""
                        <div style='background-color: #111; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #FF4B4B;'>
                            <span style='color: #FF4B4B; font-weight: bold; font-size: 12px;'>📊 {category_name.upper()} • {series_name}</span>
                            <h3 style='margin: 10px 0 5px 0; color: white;'>
                                {team1} <span style='color: #FF4B4B;'>{t1_score or 0}/{t1_wkts}</span> ({t1_overs} ov)
                                <span style='color: gray; font-size: 18px;'> vs </span> 
                                {team2} <span style='color: #FF4B4B;'>{t2_score or 0}/{t2_wkts}</span> ({t2_overs} ov)
                            </h3>
                            <p style='color: #00B4D8; margin: 0; font-size: 14px; font-weight: bold;'>💬 {status_text}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
        if not live_found:
            st.info("There are no live matches being played right now. Head over to the Upcoming Fixtures tab!")

    # ==========================================
    # TAB 2: UPCOMING FIXTURES
    # ==========================================
    with tab2:
        upcoming_matches = []
        for match_type in data['typeMatches']:
            for match_wrapper in match_type.get('seriesMatches', []):
                for match in match_wrapper.get('seriesMatches', {}).get('matches', []):
                    match_info = match.get('matchInfo', {})
                    match_state = match_info.get('state', '').lower()
                    
                    if match_state == 'preview' or match_state == 'upcoming':
                        upcoming_matches.append({
                            "Series/Tournament": match_info.get('seriesName', 'Tournament'),
                            "Fixture": f"{match_info.get('team1', {}).get('teamName')} vs {match_info.get('team2', {}).get('teamName')}",
                            "Format": match_info.get('matchFormat', 'T20'),
                            "Venue": f"{match_info.get('venueInfo', {}).get('groundName')}, {match_info.get('venueInfo', {}).get('city')}"
                        })
                        
        if upcoming_matches:
            st.dataframe(pd.DataFrame(upcoming_matches), use_container_width=True, hide_index=True)
        else:
            st.info("No upcoming match schedules available in this feed.")