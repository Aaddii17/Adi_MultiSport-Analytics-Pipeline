import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ==========================================
# SMART CACHED MULTI-API FALLBACK ENGINE
# ==========================================
@st.cache_data(ttl=90)
def _cached_api_request(url, api_key, api_host):
    """Core request engine with 90-second memory to protect limits."""
    headers = {
        "X-RapidAPI-Key": api_key,
        "X-RapidAPI-Host": api_host
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.status_code, response.json()
        return response.status_code, None
    except Exception:
        return 500, None

def fetch_cricket_stream(endpoint):
    """
    Attempts to fetch data across three different API keys.
    Shows visual diagnostics in the sidebar if a key fails.
    """
    targets = [
        {"key": st.secrets.get("CRICBUZZ_KEY_1", ""), "name": "Primary Key"},
        {"key": st.secrets.get("CRICBUZZ_KEY_2", ""), "name": "Backup Key 1"},
        {"key": st.secrets.get("CRICBUZZ_KEY_3", ""), "name": "Backup Key 2"}
    ]
    
    url = f"https://cricbuzz-cricket.p.rapidapi.com/{endpoint}"
    
    for target in targets:
        if not target["key"]:
            continue
            
        status, data = _cached_api_request(url, target["key"], "cricbuzz-cricket.p.rapidapi.com")
        
        if status == 200:
            return data
        elif status == 429:
            st.sidebar.warning(f"⚠️ {target['name']} hit its quota limit (429). Trying backup...")
        elif status == 403:
            st.sidebar.error(f"❌ {target['name']} is blocked (403). It is likely NOT subscribed to the correct 'Cricbuzz Cricket' API.")
        else:
            st.sidebar.error(f"⚠️ {target['name']} encountered a server error ({status}).")
            
    st.sidebar.error("🚨 CRITICAL: All available API keys failed or ran out of quota!")
    return None

def extract_all_matches(json_data):
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
    with st.spinner("Loading deep match analysis..."):
        scorecard_data = fetch_cricket_stream(f"mcenter/v1/{match_id}/hscard")
        
        if not scorecard_data or not isinstance(scorecard_data, dict):
            st.warning("Deep scorecard data is currently unavailable for this specific match (it may have been abandoned, washed out, or is a minor league).")
            return

        st.markdown("### 🔮 Match Insights & Analysis")
        col1, col2, col3 = st.columns(3)
        
        headers = scorecard_data.get('matchHeader', {})
        toss_winner = headers.get('tossResults', {}).get('tossWinnerName', '')
        toss_decision = headers.get('tossResults', {}).get('decision', '')
        
        toss_text = f"{toss_winner} opted to {toss_decision}" if toss_winner else "Toss info unavailable"
        
        with col1:
            st.info(f"**Toss:** {toss_text}")
        with col2:
            st.warning(f"**Status:** {headers.get('status', 'Data Pending')}")
        with col3:
            st.success(f"**Format:** {headers.get('matchFormat', 'Unknown')}")

        st.markdown("### 🏏 Detailed Scorecard")
        
        innings_list = scorecard_data.get('scoreCard', [])
        if not innings_list and 'matchScoreDetails' in scorecard_data:
            innings_list = scorecard_data['matchScoreDetails'].get('inningsScoreList', [])

        if not innings_list:
            st.warning("Batter and Bowler statistics are not populated for this match yet.")
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
    
    if "CRICBUZZ_KEY_1" not in st.secrets:
        st.warning("API Key not found in Streamlit Secrets. Please verify your variables are named CRICBUZZ_KEY_1, CRICBUZZ_KEY_2, etc.")
        return

    if st.button("🔄 Refresh API Feeds"):
        st.cache_data.clear() # Clears memory to force a fresh fetch
        st.rerun()

    tab1, tab2, tab3 = st.tabs(["🔴 Live Action", "📅 Upcoming Schedule", "🏆 Recent Results"])

    # ==========================================
    # TAB 1: LIVE MATCH TRACKER
    # ==========================================
    with tab1:
        with st.spinner("Fetching live games..."):
            live_data = fetch_cricket_stream("matches/v1/live")
            
        all_live_matches = extract_all_matches(live_data) if live_data else []
        live_dict = {}
        live_found = False
        
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
                
                live_dict[f"🔴 LIVE: {fixture_name} ({series_name})"] = match_id
                
                match_score = match.get('matchScore', {})
                s1 = match_score.get('team1Score', {}).get('inngs1', {})
                s2 = match_score.get('team2Score', {}).get('inngs1', {})
                
                d1 = f"{s1.get('score', 0)}/{s1.get('wickets', 0)} ({s1.get('overs', 0)} ov)" if 'score' in s1 else "Yet to bat"
                d2 = f"{s2.get('score', 0)}/{s2.get('wickets', 0)} ({s2.get('overs', 0)} ov)" if 'score' in s2 else "Yet to bat"

                st.markdown(f"""
                <div style='background-color: #111; padding: 20px; border-radius: 8px; margin-bottom: 15px; border-left: 4px solid #FF4B4B;'>
                    <span style='color: #FF4B4B; font-weight: bold; font-size: 12px;'>📊 {series_name}</span>
                    <h3 style='margin: 10px 0 5px 0; color: white;'>
                        {team1} <span style='color: #FF4B4B; font-size: 24px;'>{d1}</span>
                        <span style='color: gray; font-size: 16px; margin: 0 10px;'>vs</span> 
                        {team2} <span style='color: #FF4B4B; font-size: 24px;'>{d2}</span>
                    </h3>
                    <p style='color: #00B4D8; margin: 0; font-size: 14px; font-weight: bold;'>💬 {status_text}</p>
                </div>
                """, unsafe_allow_html=True)
                
        if not live_found:
            st.info("No active play happening right now. Switch to the Schedule or Recent tabs!")
            
        if live_dict:
            st.markdown("---")
            st.markdown("### 📡 Deep Analysis Scorecards")
            selected_live = st.selectbox("Select a match to load detailed player stats:", ["-- Select a Match --"] + list(live_dict.keys()), key="live_selector")
            if selected_live != "-- Select a Match --":
                render_detailed_scorecard(live_dict[selected_live])

    # ==========================================
    # TAB 2: UPCOMING FIXTURES
    # ==========================================
    with tab2:
        with st.spinner("Compiling full future schedule..."):
            upcoming_data = fetch_cricket_stream("matches/v1/upcoming")
            
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
            recent_data = fetch_cricket_stream("matches/v1/recent")
            
        all_recent_matches = extract_all_matches(recent_data) if recent_data else []
        recent_list = []
        match_dict = {}
        
        for match in all_recent_matches:
            match_info = match.get('matchInfo', {})
            if match_info.get('state', '').lower() == 'complete' and match_info.get('matchId'):
                venue = match_info.get('venueInfo', {})
                team1 = match_info.get('team1', {}).get('teamName', 'Team 1')
                team2 = match_info.get('team2', {}).get('teamName', 'Team 2')
                fixture_name = f"{team1} vs {team2}"
                
                recent_list.append({
                    "Tournament/Series": match_info.get('seriesName', 'Tournament'),
                    "Fixture": fixture_name,
                    "Result Note": match_info.get('status', 'Match Finished'),
                    "Venue": f"{venue.get('groundName', '')}, {venue.get('city', '')}"
                })
                match_dict[f"🏆 {fixture_name} - {match_info.get('seriesName')}"] = match_info.get('matchId')
                
        if recent_list:
            st.dataframe(pd.DataFrame(recent_list), use_container_width=True, hide_index=True)
            
            st.markdown("### 📊 Interactive Scorecard Viewer")
            st.info("Select a match below to fetch the detailed batter & bowler statistics.")
            selected_match = st.selectbox("Select a Past Match:", ["-- Select a Match --"] + list(match_dict.keys()), key="recent_selector")
            
            if selected_match != "-- Select a Match --":
                render_detailed_scorecard(match_dict[selected_match])
        else:
            st.info("No recent match results found.")