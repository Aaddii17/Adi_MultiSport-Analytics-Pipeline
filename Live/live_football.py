import streamlit as st
import requests
from datetime import datetime

def run_live_football():
    st.header("⚽ Real-Time Live & World Cup 2026 Center")
    st.markdown("---")
    
    api_key = st.secrets.get("FOOTBALL_API_KEY", "")
    if not api_key:
        st.error("API Key missing! Add 'FOOTBALL_API_KEY' to Streamlit Secrets.")
        return

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "livescore6.p.rapidapi.com"
    }
    
    # Added the refresh button just like your cricket dashboard!
    if st.button("🔄 Refresh Football Scores"):
        st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(["🔴 Live Right Now", "📅 Today's Schedule", "🏆 Recent Results", "🌍 FIFA World Cup 2026"])

    # ==========================================
    # TAB 1: LIVE (COMPLETELY UNTOUCHED & SAFE)
    # ==========================================
    with tab1:
        st.subheader("Currently Playing")
        try:
            url_live = "https://livescore6.p.rapidapi.com/matches/v2/list-live"
            response = requests.get(url_live, headers=headers, params={"Category": "soccer"}, timeout=10)
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
                                <h4 style='margin: 5px 0; color: white;'>{home} {home_goals} - {away_goals} {away}</h4>
                                <span style='color: #ffffff;'>⏱️ {elapsed}</span>
                            </div>
                            """, unsafe_allow_html=True)
                    
                    if match_count == 0:
                        st.info("No active matches at this exact moment.")
            else:
                st.error(f"API Error: {response.status_code}.")
        except Exception as e:
            st.error("Error connecting to LiveScore API.")

    # ==========================================
    # FETCH SCHEDULE DATA (FOR TABS 2, 3, AND 4)
    # ==========================================
    today_str = datetime.now().strftime("%Y%m%d")
    url_date = "https://livescore6.p.rapidapi.com/matches/v2/list-by-date"
    today_data = {}
    
    try:
        res_date = requests.get(url_date, headers=headers, params={"Category": "soccer", "Date": today_str}, timeout=10)
        if res_date.status_code == 200:
            today_data = res_date.json()
    except:
        pass
        
    stages_today = today_data.get('Stages', [])

    # ==========================================
    # TAB 2: UPCOMING MATCHES
    # ==========================================
    with tab2:
        st.subheader("Today's Upcoming Schedule")
        if not stages_today:
            st.warning("Schedule data is currently unavailable.")
        else:
            upcoming_found = False
            for stage in stages_today:
                league = stage.get('Snm', 'Unknown')
                country = stage.get('Cnm', 'Unknown')
                for match in stage.get('Events', []):
                    eps = str(match.get('Eps', ''))
                    # If match hasn't started, LiveScore marks it 'NS' or gives a time like '15:30'
                    if eps == 'NS' or ':' in eps:
                        upcoming_found = True
                        home = match.get('T1', [{}])[0].get('Nm', 'Home')
                        away = match.get('T2', [{}])[0].get('Nm', 'Away')
                        
                        st.markdown(f"""
                        <div style='background-color: #1e1e1e; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #f39c12;'>
                            <small style='color: #f39c12;'>📅 {country} - {league}</small><br>
                            <b style='color: white;'>{home} vs {away}</b> <span style='color: #bdc3c7; font-size: 14px;'>| 🕒 {eps}</span>
                        </div>
                        """, unsafe_allow_html=True)
            if not upcoming_found:
                st.info("No more upcoming matches scheduled for today.")

    # ==========================================
    # TAB 3: RECENT RESULTS
    # ==========================================
    with tab3:
        st.subheader("Today's Completed Matches")
        if not stages_today:
            st.warning("Results data is currently unavailable.")
        else:
            recent_found = False
            for stage in stages_today:
                league = stage.get('Snm', 'Unknown')
                country = stage.get('Cnm', 'Unknown')
                for match in stage.get('Events', []):
                    eps = str(match.get('Eps', ''))
                    # LiveScore uses FT (Full Time), AET (After Extra Time), AP (After Penalties)
                    if eps in ['FT', 'AET', 'AP']:
                        recent_found = True
                        home = match.get('T1', [{}])[0].get('Nm', 'Home')
                        away = match.get('T2', [{}])[0].get('Nm', 'Away')
                        home_goals = match.get('Tr1', '0')
                        away_goals = match.get('Tr2', '0')
                        
                        st.markdown(f"""
                        <div style='background-color: #1e1e1e; padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #3498db;'>
                            <small style='color: #3498db;'>✅ {country} - {league} ({eps})</small><br>
                            <b style='color: white;'>{home} {home_goals} - {away_goals} {away}</b>
                        </div>
                        """, unsafe_allow_html=True)
            if not recent_found:
                st.info("No completed matches recorded for today yet.")

    # ==========================================
    # TAB 4: FIFA WORLD CUP 2026
    # ==========================================
    with tab4:
        st.subheader("🏆 FIFA World Cup 2026 - Today's Action")
        if not stages_today:
             st.info("World Cup data is syncing.")
        else:
            wc_found = False
            for stage in stages_today:
                league = stage.get('Snm', 'Unknown')
                country = stage.get('Cnm', 'Unknown')
                # Filter strictly for World Cup matches
                if 'World Cup' in league or 'World' in country:
                    for match in stage.get('Events', []):
                        wc_found = True
                        home = match.get('T1', [{}])[0].get('Nm', 'Home')
                        away = match.get('T2', [{}])[0].get('Nm', 'Away')
                        home_goals = match.get('Tr1', '')
                        away_goals = match.get('Tr2', '')
                        eps = match.get('Eps', '')
                        
                        score_str = f"{home_goals} - {away_goals}" if home_goals else "vs"
                        
                        st.markdown(f"""
                        <div style='background-color: #2b2b2b; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 4px solid #f1c40f;'>
                            <small style='color: #f1c40f;'>🌍 {league}</small><br>
                            <h4 style='margin: 5px 0; color: white;'>{home} {score_str} {away}</h4>
                            <span style='color: #bdc3c7;'>Status: {eps}</span>
                        </div>
                        """, unsafe_allow_html=True)
            if not wc_found:
                st.info("No FIFA World Cup matches scheduled for today. Check back tomorrow!")