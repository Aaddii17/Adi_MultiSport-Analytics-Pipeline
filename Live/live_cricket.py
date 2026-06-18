import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# ==========================================
# SMART CACHED MULTI-API FALLBACK ENGINE
# ==========================================
@st.cache_data(ttl=90)  # Core limit protection trick
def fetch_cricket_stream(endpoint):
    """
    Attempts to fetch data across three different API keys/providers.
    Caches successful results for 90 seconds to save your quota limits.
    """
    # Define potential endpoints/hosts mapping if structure differences arise
    # For these three Cricbuzz mirrors, the paths remain uniform.
    targets = [
        {"key": st.secrets.get("CRICBUZZ_KEY_1", ""), "host": "cricbuzz-cricket.p.rapidapi.com"},
        {"key": st.secrets.get("CRICBUZZ_KEY_2", ""), "host": "cricbuzz-cricket.p.rapidapi.com"},
        {"key": st.secrets.get("CRICBUZZ_KEY_3", ""), "host": "cricbuzz-cricket.p.rapidapi.com"}
    ]
    
    url = f"https://cricbuzz-cricket.p.rapidapi.com/{endpoint}"
    
    for i, target in enumerate(targets, start=1):
        if not target["key"]:
            continue  # Skip if key is missing from secrets
            
        headers = {
            "X-RapidAPI-Key": target["key"],
            "X-RapidAPI-Host": target["host"]
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=8)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass # Suppress error and cycle to the next backup pipeline
            
    return None

def extract_all_matches(json_data):
    """Recursively parses nested arrays to locate standard match objects."""
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
    """Fetches deep innings data on-demand only when selected."""
    scorecard_data = fetch_cricket_stream(f"mcenter/v1/{match_id}/hscard")
    
    if not scorecard_data or not isinstance(scorecard_data, dict):
        st.warning("Deep metrics are currently unavailable or loading. (Common for abandoned or minor matches).")
        return

    st.markdown("### 🔮 Match Insights")
    headers = scorecard_data.get('matchHeader', {})
    toss_winner = headers.get('tossResults', {}).get('tossWinnerName', '')
    toss_decision = headers.get('tossResults', {}).get('decision', '')
    toss_text = f"{toss_winner} elected to {toss_decision}" if toss_winner else "Toss pending"
    
    c1, c2 = st.columns(2)
    c1.info(f"**Toss Result:** {toss_text}")
    c2.success(f"**Official Status:** {headers.get('status', 'Live')}")

    st.markdown("### 🏏 Full Scorecard Data")
    innings_list = scorecard_data.get('scoreCard', [])
    if not innings_list and 'matchScoreDetails' in scorecard_data:
        innings_list = scorecard_data['matchScoreDetails'].get('inningsScoreList', [])

    if not innings_list:
        st.info("Player analytics have not been compiled yet for this fixture instance.")
        return

    for inning in innings_list:
        inning_name = inning.get('batTeamDetails', {}).get('batTeamName', 'Team')
        runs = inning.get('scoreDetails', {}).get('runs', 0)
        wickets = inning.get('scoreDetails', {}).get('wickets', 0)
        overs = inning.get('scoreDetails', {}).get('overs', 0.0)
        
        with st.expander(f"👉 {inning_name} Innings: {runs}/{wickets} ({overs} Ov)", expanded=True):
            # Batting Parsing
            batters = inning.get('batTeamDetails', {}).get('batsmenData', {})
            b_rows = []
            for _, b in batters.items():
                b_rows.append({
                    "Batter": b.get('batName', 'Unknown'),
                    "Status": b.get('outDesc', 'Not Out'),
                    "Runs": b.get('runs', 0),
                    "Balls": b.get('balls', 0),
                    "4s": b.get('boundaries', 0),
                    "6s": b.get('sixers', 0),
                    "SR": b.get('strikeRate', 0)
                })
            if b_rows:
                st.dataframe(pd.DataFrame(b_rows), use_container_width=True, hide_index=True)
                
            # Bowling Parsing
            bowlers = inning.get('bowlTeamDetails', {}).get('bowlersData', {})
            bowl_rows = []
            for _, bw in bowlers.items():
                bowl_rows.append({
                    "Bowler": bw.get('bowlName', 'Unknown'),
                    "Overs": bw.get('overs', 0),
                    "Maidens": bw.get('maidens', 0),
                    "Runs": bw.get('runs', 0),
                    "Wickets": bw.get('wickets', 0),
                    "Economy": bw.get('economy', 0)
                })
            if bowl_rows:
                st.dataframe(pd.DataFrame(bowl_rows), use_container_width=True, hide_index=True)

# ==========================================
# MAIN SIDEBAR CORE INTERFACE
# ==========================================
def run_live_cricket():
    st.header("🔴 Live Match Center & Global Schedule")
    st.markdown("---")
    
    # Check if vault architecture is mapped
    if not st.secrets.get("CRICBUZZ_KEY_1"):
        st.error("No active API stream architecture mapped to the secrets console storage.")
        return

    tab1, tab2, tab3 = st.tabs(["🔴 Live Interfaces", "📅 Future Fixtures", "🏆 Completed Results"])

    # --- TAB 1: LIVE ACTION ---
    with tab1:
        with st.spinner("Streaming live signals from fallback cluster..."):
            live_payload = fetch_cricket_stream("matches/v1/live")
            
        all_live = extract_all_matches(live_payload) if live_payload else []
        live_tracker = {}
        
        for m in all_live:
            info = m.get('matchInfo', {})
            state = info.get('state', '').lower()
            m_id = info.get('matchId')
            
            valid_live = ['inprogress', 'live', 'innings break', 'toss', 'lunch', 'tea', 'stumps', 'delay', 'rain']
            if state in valid_live and m_id:
                series = info.get('seriesName', 'Match Instance')
                t1 = info.get('team1', {}).get('teamName', 'T1')
                t2 = info.get('team2', {}).get('teamName', 'T2')
                label = f"{t1} vs {t2}"
                
                live_tracker[f"🔴 LIVE: {label} ({series})"] = m_id
                
                # Visual Box Render
                score = m.get('matchScore', {})
                s1 = score.get('team1Score', {}).get('inngs1', {})
                s2 = score.get('team2Score', {}).get('inngs1', {})
                
                d1 = f"{s1.get('score', 0)}/{s1.get('wickets', 0)} ({s1.get('overs', 0)} ov)" if 'score' in s1 else "Yet to bat"
                d2 = f"{s2.get('score', 0)}/{s2.get('wickets', 0)} ({s2.get('overs', 0)} ov)" if 'score' in s2 else "Yet to bat"
                
                st.markdown(f"""
                <div style='background-color: #111; padding: 18px; border-radius: 8px; margin-bottom: 12px; border-left: 4px solid #FF4B4B;'>
                    <span style='color: #FF4B4B; font-weight: bold; font-size: 11px;'>📊 {series}</span>
                    <h4 style='margin: 8px 0; color: white;'>
                        {t1} <span style='color: #FF4B4B;'>{d1}</span> vs {t2} <span style='color: #FF4B4B;'>{d2}</span>
                    </h4>
                    <p style='color: #00B4D8; margin: 0; font-size: 13px;'>💬 {info.get('status', 'Play ongoing')}</p>
                </div>
                """, unsafe_allow_html=True)
                
        if live_tracker:
            st.markdown("---")
            selected_live = st.selectbox("Inspect Active Live Statistics:", ["-- Choose Match --"] + list(live_tracker.keys()), key="live_drill")
            if selected_live != "-- Choose Match --":
                render_detailed_scorecard(live_tracker[selected_live])
        else:
            st.info("No international or domestic tournament clusters are actively playing right now.")

    # --- TAB 2: FUTURE SCHEDULES ---
    with tab2:
        with st.spinner("Extracting international calendars..."):
            future_payload = fetch_cricket_stream("matches/v1/upcoming")
            
        all_future = extract_all_matches(future_payload) if future_payload else []
        f_list = []
        
        for m in all_future:
            info = m.get('matchInfo', {})
            if info.get('state', '').lower() in ['preview', 'upcoming']:
                loc = info.get('venueInfo', {})
                f_list.append({
                    "Date/Time Window": format_timestamp(info.get('startDate')),
                    "Tournament/Series": info.get('seriesName', 'International Tour'),
                    "Fixture Details": f"{info.get('team1', {}).get('teamName')} vs {info.get('team2', {}).get('teamName')}",
                    "Ground Location": f"{loc.get('groundName', '')}, {loc.get('city', '')}"
                })
        if f_list:
            st.dataframe(pd.DataFrame(f_list), use_container_width=True, hide_index=True)
        else:
            st.info("No upcoming entries detected inside this API feed sector.")

    # --- TAB 3: COMPLETED OUTCOMES ---
    with tab3:
        with st.spinner("Extracting historical day results..."):
            past_payload = fetch_cricket_stream("matches/v1/recent")
            
        all_past = extract_all_matches(past_payload) if past_payload else []
        past_tracker = {}
        past_display_list = []
        
        for m in all_past:
            info = m.get('matchInfo', {})
            if info.get('state', '').lower() == 'complete' and info.get('matchId'):
                t1 = info.get('team1', {}).get('teamName', 'T1')
                t2 = info.get('team2', {}).get('teamName', 'T2')
                label = f"{t1} vs {t2}"
                
                past_display_list.append({
                    "Tournament/Series": info.get('seriesName', 'Series'),
                    "Fixture Details": label,
                    "Final Result Outcome": info.get('status', 'Finished')
                })
                past_tracker[f"🏆 {label} - {info.get('seriesName')}"] = info.get('matchId')
                
        if past_display_list:
            st.dataframe(pd.DataFrame(past_display_list), use_container_width=True, hide_index=True)
            st.markdown("---")
            selected_past = st.selectbox("Inspect Historical Match Scorecard:", ["-- Choose Match --"] + list(past_tracker.keys()), key="past_drill")
            if selected_past != "-- Choose Match --":
                render_detailed_scorecard(past_tracker[selected_past])
        else:
            st.info("No historical entries located inside the current data block.")