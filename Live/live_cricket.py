import streamlit as st
import requests
import pandas as pd
from datetime import datetime

def fetch_api_data(endpoint):
    """Fetches data with a smart Fallback mechanism to protect API limits."""
    url = f"https://cricbuzz-cricket.p.rapidapi.com/{endpoint}"
    
    primary_key = st.secrets.get("CRICBUZZ_API_KEY", "")
    backup_key = st.secrets.get("CRICBUZZ_BACKUP_KEY", "")
    
    headers_primary = {
        "X-RapidAPI-Key": primary_key,
        "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"
    }
    
    try:
        response = requests.get(url, headers=headers_primary, timeout=10)
        if response.status_code == 200:
            return response.json()
    except Exception:
        pass 

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

def render_detailed_scorecard(match_id):
    """Safely extracts and renders the deep scorecard and analysis."""
    with st.spinner("Loading deep match analysis & scorecards..."):
        scorecard_data = fetch_api_data(f"mcenter/v1/{match_id}/hscard")
        
        if not scorecard_data or not isinstance(scorecard_data, dict):
            st.error("Scorecard data is currently unavailable for this match.")
            return

        # 1. Match Insights & Predictions Section
        st.markdown("### 🔮 Match Insights & Analysis")
        col1, col2, col3 = st.columns(3)
        
        # Safely extract headers (Cricbuzz changes keys often, so we use .get())
        headers = scorecard_data.get('matchHeader', {})
        toss_info = headers.get('tossResults', {}).get('tossWinnerName', 'Unknown')
        toss_decision = headers.get('tossResults', {}).get('decision', '')
        match_state = headers.get('state', 'Unknown')
        
        with col1:
            st.info(f"**Toss:** {toss_info} opted to {toss_decision}")
        with col2:
            st.warning(f"**Status:** {headers.get('status', 'In Progress')}")
        with col3:
            st.success(f"**State:** {match_state.upper()}")

        # 2. Detailed Scorecard Section
        st.markdown("### 🏏 Detailed Scorecard")
        
        # Handle Cricbuzz's changing dictionary keys safely without KeyError
        innings_list = scorecard_data.get('scoreCard', [])
        if not innings_list and 'matchScoreDetails' in scorecard_data:
            innings_list = scorecard_data['matchScoreDetails'].get('inningsScoreList', [])

        if not innings_list:
            st.warning("Detailed batter/bowler stats are not populated by the API yet.")
            return

        for inning in innings_list:
            inning_name = inning.get('batTeamDetails', {}).get('batTeamName', 'Innings')
            runs = inning.get('scoreDetails', {}).get('runs', 0)
            wickets = inning.get('scoreDetails', {}).get('wickets', 0)
            overs = inning.get('scoreDetails', {}).get('overs', 0.0)
            
            with st.expander(f"👉 {inning_name} Innings - {runs}/{wickets} ({overs} Ov)", expanded=True):
                # Batters Table
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
                
                # Bowlers Table
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

def run_live_cricket():
    st.header("🔴 Live Match Center & Global Schedule")
    st.markdown("---")
    
    if "CRICBUZZ_API_KEY" not in st.secrets:
        st.warning("API Key not found in Streamlit Secrets.")
        return

    if st.button("🔄 Refresh API Feeds"):
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔴 Live Action & Scorecards", "📅 Upcoming Schedule", "🏆 Recent Results"])

    # ==========================================
    # TAB 1: LIVE MATCH TRACKER (NOW WITH DRILL-DOWN)
    # ==========================================
    with tab1:
        with st.spinner("Fetching live games..."):
            live_data = fetch_api_data("matches/v1/live")
            
        all_live_matches = extract_all_matches(live_data) if live_data else []
        live_dict = {}
        
        for match in all_live_matches:
            match_info = match.get('matchInfo', {})
            state = match_info.get('state', '').lower()
            match_id = match_info.get('matchId')
            
            active_states = ['inprogress', 'live', 'innings break', 'toss', 'lunch', 'tea', 'stumps', 'delay', 'rain']
            if state in active_states and match_id:
                series_name = match_info.get('seriesName', 'International Match')
                team1 = match_info.get('team1', {}).get('teamName', 'Team 1')
                team2 = match_info.get('team2', {}).get('teamName', 'Team 2')
                fixture_name = f"{team1} vs {team2}"
                live_dict[f"🔴 LIVE: {fixture_name} ({series_name})"] = match_id
                
        if live_dict:
            st.markdown("### 📡 Select an Active Match for Deep Analysis")
            selected_live = st.selectbox("Choose a Live Match:", ["-- Select a Match --"] + list(live_dict.keys()), key="live_selector")
            
            if selected_live != "-- Select a Match --":
                render_detailed_scorecard(live_dict[selected_live])
        else:
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
            if match_info.get('state', '').lower() in ['preview', 'upcoming']:
                venue = match_info.get('venueInfo', {})
                upcoming_list.append({
                    "Date & Time": format_timestamp(match_info.get('startDate')),
                    "Tournament": match_info.get('seriesName', 'Tournament'),
                    "Fixture": f"{match_info.get('team1', {}).get('teamName')} vs {match_info.get('team2', {}).get('teamName')}",
                    "Venue": f"{venue.get('groundName', '')}, {venue.get('city', '')}"
                })
                
        if upcoming_list:
            st.dataframe(pd.DataFrame(upcoming_list), use_container_width=True, hide_index=True)
        else:
            st.info("No upcoming match schedules found.")

    # ==========================================
    # TAB 3: RECENT RESULTS
    # ==========================================
    with tab3:
        with st.spinner("Fetching completed matches..."):
            recent_data = fetch_api_data("matches/v1/recent")
            
        all_recent_matches = extract_all_matches(recent_data) if recent_data else []
        match_dict = {}
        
        for match in all_recent_matches:
            match_info = match.get('matchInfo', {})
            if match_info.get('state', '').lower() == 'complete' and match_info.get('matchId'):
                team1 = match_info.get('team1', {}).get('teamName', 'Team 1')
                team2 = match_info.get('team2', {}).get('teamName', 'Team 2')
                fixture_name = f"{team1} vs {team2}"
                match_dict[f"🏆 {fixture_name} - {match_info.get('seriesName')}"] = match_info.get('matchId')
                
        if match_dict:
            st.markdown("### 📊 Interactive Scorecard Viewer")
            selected_match = st.selectbox("Select a Past Match:", ["-- Select a Match --"] + list(match_dict.keys()), key="recent_selector")
            
            if selected_match != "-- Select a Match --":
                render_detailed_scorecard(match_dict[selected_match])
        else:
            st.info("No recent match results found.")