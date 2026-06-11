import streamlit as st
import requests
import pandas as pd

def fetch_live_matches(api_key):
    """Fetches real-time JSON data from the Cricbuzz API."""
    url = "https://cricbuzz-cricket.p.rapidapi.com/matches/v1/live"
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception:
        return None

def extract_all_matches(json_data):
    """Recursively digs through complex JSON to find every single match block."""
    matches = []
    if isinstance(json_data, dict):
        if 'matchInfo' in json_data:
            matches.append(json_data)
        else:
            for key, value in json_data.items():
                matches.extend(extract_all_matches(value))
    elif isinstance(json_data, list):
        for item in json_data:
            matches.extend(extract_all_matches(item))
    return matches

def run_live_cricket():
    st.header("🔴 Live Match Center & Schedule")
    st.markdown("---")
    
    # Secure Vault Connection
    if "CRICBUZZ_API_KEY" in st.secrets:
        API_KEY = st.secrets["CRICBUZZ_API_KEY"]
    else:
        st.warning("API Key not found in Streamlit Secrets.")
        return

    if st.button("🔄 Refresh Live Scores"):
        st.rerun()

    with st.spinner("Connecting to global cricket feeds..."):
        data = fetch_live_matches(API_KEY)

    if not data:
        st.error("Could not connect to the API. It might be rate-limited.")
        return

    # Extract all matches regardless of API nesting structure
    all_matches = extract_all_matches(data)
    
    if not all_matches:
        st.info("No matches are currently populated in the live feed.")
        return

    tab1, tab2 = st.tabs(["🔴 Live Match Tracker", "📅 Upcoming Fixtures"])

    # ==========================================
    # TAB 1: LIVE MATCH TRACKER
    # ==========================================
    with tab1:
        live_found = False
        for match in all_matches:
            match_info = match.get('matchInfo', {})
            state = match_info.get('state', '').lower()
            
            # Show matches even if they are on a break, toss, or delayed
            active_states = ['inprogress', 'live', 'innings break', 'toss', 'lunch', 'tea', 'stumps', 'delay', 'rain']
            
            if state in active_states:
                live_found = True
                series_name = match_info.get('seriesName', 'International Match')
                status_text = match_info.get('status', 'Match underway')
                team1 = match_info.get('team1', {}).get('teamName', 'Team 1')
                team2 = match_info.get('team2', {}).get('teamName', 'Team 2')
                
                # Safely extract scores
                match_score = match.get('matchScore', {})
                t1_data = match_score.get('team1Score', {}).get('inngs1', {})
                t1_display = f"{t1_data.get('score', 0)}/{t1_data.get('wickets', 0)} ({t1_data.get('overs', 0)} ov)" if 'score' in t1_data else "Yet to bat"
                
                t2_data = match_score.get('team2Score', {}).get('inngs1', {})
                t2_display = f"{t2_data.get('score', 0)}/{t2_data.get('wickets', 0)} ({t2_data.get('overs', 0)} ov)" if 'score' in t2_data else "Yet to bat"

                st.markdown(f"""
                <div style='background-color: #111; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #FF4B4B;'>
                    <span style='color: #FF4B4B; font-weight: bold; font-size: 12px;'>📊 {series_name}</span>
                    <h3 style='margin: 10px 0 5px 0; color: white;'>
                        {team1} <span style='color: #FF4B4B; font-size: 24px;'>{t1_display}</span>
                        <span style='color: gray; font-size: 16px; margin: 0 10px;'>vs</span> 
                        {team2} <span style='color: #FF4B4B; font-size: 24px;'>{t2_display}</span>
                    </h3>
                    <p style='color: #00B4D8; margin: 0; font-size: 14px; font-weight: bold;'>💬 {status_text}</p>
                </div>
                """, unsafe_allow_html=True)
                
        if not live_found:
            st.info("No active play happening this exact minute (matches might be finished or upcoming). Check the Next Fixtures tab!")

    # ==========================================
    # TAB 2: UPCOMING FIXTURES
    # ==========================================
    with tab2:
        upcoming_matches = []
        for match in all_matches:
            match_info = match.get('matchInfo', {})
            state = match_info.get('state', '').lower()
            
            if state in ['preview', 'upcoming']:
                venue = match_info.get('venueInfo', {})
                upcoming_matches.append({
                    "Tournament": match_info.get('seriesName', 'Tournament'),
                    "Fixture": f"{match_info.get('team1', {}).get('teamName')} vs {match_info.get('team2', {}).get('teamName')}",
                    "Status": match_info.get('status', 'Upcoming'),
                    "Location": f"{venue.get('groundName', '')}, {venue.get('city', '')}"
                })
                
        if upcoming_matches:
            st.dataframe(pd.DataFrame(upcoming_matches), use_container_width=True, hide_index=True)
        else:
            st.info("No upcoming match schedules found in the current feed.")