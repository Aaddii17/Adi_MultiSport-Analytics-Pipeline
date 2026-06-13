import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def fetch_api_data(endpoint):
    """Fetches data with a smart Fallback mechanism to protect API limits."""
    url = f"https://cricbuzz-cricket.p.rapidapi.com/{endpoint}"
    
    primary_key = st.secrets.get("CRICBUZZ_API_KEY", "")
    backup_key = st.secrets.get("CRICBUZZ_BACKUP_KEY", "")
    
    # ATTEMPT 1: Primary API
    headers_primary = {
        "X-RapidAPI-Key": primary_key,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers_primary, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass # Silently fail and try backup

    # ATTEMPT 2: Backup API
    if backup_key:
        headers_backup = {
            "X-RapidAPI-Key": backup_key,
            "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
        }
        try:
            backup_response = requests.get(url, headers=headers_backup, timeout=10)
            if backup_response.status_code == 200:
                return backup_response.json()
        except Exception:
            return None
            
    return None

def extract_all_matches(json_data):
    """Recursively parses the complex nested JSON structure."""
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

def format_timestamp(timestamp_ms):
    if not timestamp_ms:
        return "TBD"
    try:
        dt = datetime.fromtimestamp(int(timestamp_ms) / 1000)
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except Exception:
        return "TBD"

def run_live_cricket():
    st.header("🔴 Live Match Center & Global Schedule")
    st.markdown("---")
    
    if "CRICBUZZ_API_KEY" not in st.secrets:
        st.warning("API Key not found in Streamlit Secrets.")
        return

    if st.button("🔄 Refresh Matches"):
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔴 Live Action", "📅 Upcoming Schedule", "🏆 Recent Results"])

    # ==========================================
    # TAB 1: LIVE MATCH TRACKER
    # ==========================================
    with tab1:
        with st.spinner("Fetching live games..."):
            live_data = fetch_api_data("matches/v1/live")
            
        all_live_matches = extract_all_matches(live_data) if live_data else []
        live_found = False
        live_dict = {}
        
        for match in all_live_matches:
            match_info = match.get('matchInfo', {})
            state = match_info.get('state', '').lower()
            match_id = match_info.get('matchId')
            
            active_states = ['inprogress', 'live', 'innings break', 'toss', 'lunch', 'tea', 'stumps', 'delay', 'rain']
            if state in active_states and match_id:
                live_found = True
                series_name = match_info.get('seriesName', 'International Match')
                status_text = match_info.get('status', 'Match underway')
                team1 = match_info.get('team1', {}).get('teamName', 'Team 1')
                team2 = match_info.get('team2', {}).get('teamName', 'Team 2')
                fixture_name = f"{team1} vs {team2}"
                
                live_dict[f"{fixture_name} ({series_name})"] = match_id
                
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
            st.info("No active play happening right now. Switch to the Schedule or Recent tabs!")

    # ==========================================
    # TAB 2: UPCOMING FIXTURES
    # ==========================================
    with tab2:
        with st.spinner("Compiling full future schedule..."):
            upcoming_data = fetch_api_data("matches/v1/upcoming")
            
        all_upcoming_matches = extract_all_matches(upcoming_data) if upcoming_data else []
        upcoming_list = []
        
        for match in all_upcoming_matches:
            match_info = match.get('matchInfo', {})
            state = match_info.get('state', '').lower()
            
            if state in ['preview', 'upcoming']:
                venue = match_info.get('venueInfo', {})
                start_time = format_timestamp(match_info.get('startDate'))
                
                upcoming_list.append({
                    "Date & Time": start_time,
                    "Tournament": match_info.get('seriesName', 'Tournament'),
                    "Fixture": f"{match_info.get('team1', {}).get('teamName')} vs {match_info.get('team2', {}).get('teamName')}",
                    "Venue": f"{venue.get('groundName', '')}, {venue.get('city', '')}"
                })
                
        if upcoming_list:
            st.dataframe(pd.DataFrame(upcoming_list), use_container_width=True, hide_index=True)
        else:
            st.info("No upcoming match schedules found.")

    # ==========================================
    # TAB 3: RECENT RESULTS & DETAILED SCORECARDS
    # ==========================================
    with tab3:
        with st.spinner("Fetching completed matches..."):
            recent_data = fetch_api_data("matches/v1/recent")
            
        all_recent_matches = extract_all_matches(recent_data) if recent_data else []
        recent_list = []
        match_dict = {}
        
        for match in all_recent_matches:
            match_info = match.get('matchInfo', {})
            state = match_info.get('state', '').lower()
            match_id = match_info.get('matchId')
            
            if state == 'complete' and match_id:
                venue = match_info.get('venueInfo', {})
                team1 = match_info.get('team1', {}).get('teamName', 'Team 1')
                team2 = match_info.get('team2', {}).get('teamName', 'Team 2')
                fixture_name = f"{team1} vs {team2}"
                
                recent_list.append({
                    "Tournament/Series": match_info.get('seriesName', 'Tournament'),
                    "Fixture": fixture_name,
                    "Result Note": match_info.get('status', 'Match Finished')
                })
                match_dict[f"{fixture_name} - {match_info.get('seriesName')}"] = match_id
                
        if recent_list:
            st.dataframe(pd.DataFrame(recent_list), use_container_width=True, hide_index=True)
            
            st.markdown("### 📊 Interactive Scorecard Viewer")
            st.info("Select a match below to fetch the detailed batter & bowler statistics.")
            
            selected_match = st.selectbox("Select Match:", ["-- Select a Match --"] + list(match_dict.keys()))
            
            if selected_match != "-- Select a Match --":
                selected_match_id = match_dict[selected_match]
                
                with st.spinner("Fetching detailed scorecard..."):
                    scorecard_data = fetch_api_data(f"mcenter/v1/{selected_match_id}/hscard")
                    
                    if scorecard_data and 'scoreCard' in scorecard_data:
                        for inning in scorecard_data['scoreCard']:
                            inning_name = inning.get('batTeamDetails', {}).get('batTeamName', 'Innings')
                            runs = inning.get('scoreDetails', {}).get('runs', 0)
                            wickets = inning.get('scoreDetails', {}).get('wickets', 0)
                            overs = inning.get('scoreDetails', {}).get('overs', 0.0)
                            
                            with st.expander(f"🏏 {inning_name} - {runs}/{wickets} ({overs} Ov)", expanded=True):
                                # Extract Batters
                                batter_data = inning.get('batTeamDetails', {}).get('batsmenData', {})
                                b_list = []
                                for b_id, b_info in batter_data.items():
                                    b_list.append({
                                        "Batter": b_info.get('batName', 'Unknown'),
                                        "Dismissal": b_info.get('outDesc', ''),
                                        "R": b_info.get('runs', 0),
                                        "B": b_info.get('balls', 0),
                                        "4s": b_info.get('boundaries', 0),
                                        "6s": b_info.get('sixers', 0),
                                        "SR": b_info.get('strikeRate', 0)
                                    })
                                if b_list:
                                    st.markdown("**Batting**")
                                    st.dataframe(pd.DataFrame(b_list), use_container_width=True, hide_index=True)
                                
                                # Extract Bowlers
                                bowler_data = inning.get('bowlTeamDetails', {}).get('bowlersData', {})
                                bowl_list = []
                                for bw_id, bw_info in bowler_data.items():
                                    bowl_list.append({
                                        "Bowler": bw_info.get('bowlName', 'Unknown'),
                                        "O": bw_info.get('overs', 0),
                                        "M": bw_info.get('maidens', 0),
                                        "R": bw_info.get('runs', 0),
                                        "W": bw_info.get('wickets', 0),
                                        "Econ": bw_info.get('economy', 0)
                                    })
                                if bowl_list:
                                    st.markdown("**Bowling**")
                                    st.dataframe(pd.DataFrame(bowl_list), use_container_width=True, hide_index=True)
                    else:
                        st.error("Detailed scorecard is not available for this match yet.")
        else:
            st.info("No recent match results found.")