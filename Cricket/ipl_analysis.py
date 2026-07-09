import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==========================================
# DATA LOADING & MERGING STRATEGY
# ==========================================
@st.cache_data
def load_and_merge_ipl_data():
    """
    Loads historical IPL data and merges it dynamically with the new 2026 delivery data.
    Ensures all-time stats are automatically updated.
    """
    df_history_deliveries = pd.DataFrame()
    df_2026_deliveries = pd.DataFrame()

    # 1. Load User's Historical Parquet File
    parquet_path = "data/ipl_ball_by_ball_2008_2025.parquet"
    if os.path.exists(parquet_path):
        df_history_deliveries = pd.read_parquet(parquet_path)
    else:
        history_dir = "data" if os.path.exists("data/historical_deliveries.csv") else "Data"
        try:
            df_history_deliveries = pd.read_csv(f"{history_dir}/historical_deliveries.csv")
        except FileNotFoundError:
            pass 

    # 2. Load 2026 Kaggle Data (Handling Case Sensitivity)
    ipl_2026_dir = "data/IPL_2026" if os.path.exists("data/IPL_2026/ipl_2026_deliveries.csv") else "Data/IPL_2026"
    try:
        # Load the specific 2026 delivery file you found
        df_2026_deliveries = pd.read_csv(f"{ipl_2026_dir}/ipl_2026_deliveries.csv")
        
        # --- CRITICAL: Translate 2026 Columns to Match Historical Data ---
        delivery_mapping = {
            'match_no': 'match_id',
            'striker': 'batter',
            'batsman': 'batter',
            'runs_of_bat': 'runs_batter',
            'batsman_runs': 'runs_batter',
            'wicket_type': 'wicket_kind',
            'dismissal_kind': 'wicket_kind',
            'player_dismissed': 'player_out'
        }
        df_2026_deliveries.rename(columns=delivery_mapping, inplace=True)

        # Ensure seasons are set correctly
        if 'season' not in df_2026_deliveries.columns:
            df_2026_deliveries['season'] = '2026'
        else:
            df_2026_deliveries['season'] = df_2026_deliveries['season'].astype(str)
            
    except FileNotFoundError:
        st.warning(f"⚠️ Could not find '{ipl_2026_dir}/ipl_2026_deliveries.csv'. Ensure the file is present.")

    # 3. Merge Datasets Seamlessly
    all_deliveries = pd.concat([df_history_deliveries, df_2026_deliveries], ignore_index=True)

    # 4. Synthesize Match-Level Data from Deliveries
    # Since we only have delivery data for 2026, we must extract match-level info from it
    all_matches = pd.DataFrame()
    if not all_deliveries.empty and 'match_id' in all_deliveries.columns:
        # Extract unique match info
        match_cols = [col for col in ['match_id', 'season', 'date', 'venue', 'city'] if col in all_deliveries.columns]
        if match_cols:
            all_matches = all_deliveries[match_cols].drop_duplicates(subset=['match_id']).copy()

            # Determine teams per match
            if 'batting_team' in all_deliveries.columns and 'bowling_team' in all_deliveries.columns:
                teams = all_deliveries.groupby('match_id')[['batting_team', 'bowling_team']].first().reset_index()
                all_matches = all_matches.merge(teams, on='match_id', how='left')

            # Determine Match Winner (Rough estimate based on total runs)
            if 'runs_batter' in all_deliveries.columns and 'extras' in all_deliveries.columns and 'batting_team' in all_deliveries.columns:
                all_deliveries['total_runs'] = pd.to_numeric(all_deliveries['runs_batter'], errors='coerce').fillna(0) + pd.to_numeric(all_deliveries['extras'], errors='coerce').fillna(0)
                team_scores = all_deliveries.groupby(['match_id', 'batting_team'])['total_runs'].sum().reset_index()
                
                # Find the team with max runs per match
                idx = team_scores.groupby('match_id')['total_runs'].idxmax()
                winners = team_scores.loc[idx, ['match_id', 'batting_team']]
                winners.rename(columns={'batting_team': 'match_won_by'}, inplace=True)
                all_matches = all_matches.merge(winners, on='match_id', how='left')

            # Ensure season is clean string for dropdown
            if 'season' in all_matches.columns:
                all_matches['season'] = all_matches['season'].astype(str).str.replace(r'\.0$', '', regex=True)

    return all_matches, all_deliveries

# ==========================================
# MAIN DASHBOARD FUNCTION
# ==========================================
def run_ipl_analysis():
    st.header("🏏 IPL Analytics Hub")
    st.markdown("---")
    
    with st.spinner("Analyzing IPL historical records and merging 2026 data..."):
        matches, deliveries = load_and_merge_ipl_data()
    
    if matches.empty or deliveries.empty:
        st.error("No IPL data available. Please check your Data folder.")
        return

    # --- SEASON DROPDOWN ---
    season_list = []
    if 'season' in matches.columns:
        season_list = sorted(matches['season'].dropna().unique().tolist(), reverse=True)
        
    seasons = ["All-Time"] + season_list
    st.write("🗓️ **Select IPL Season:**")
    selected_season = st.selectbox("Season Dropdown", seasons, label_visibility="collapsed", key="ipl_season")

    # --- DATA FILTERING ---
    if selected_season != "All-Time":
        filtered_matches = matches[matches['season'] == selected_season]
        filtered_deliveries = deliveries[deliveries['season'].astype(str) == selected_season]
    else:
        filtered_matches = matches
        filtered_deliveries = deliveries

    tab1, tab2 = st.tabs(["📊 Tournament Leaderboard & History", "🔍 Match Scorecard Inspector"])

    # ==========================================
    # TAB 1: TOURNAMENT STATS & CHAMPIONS
    # ==========================================
    with tab1:
        total_matches = len(filtered_matches)
        
        # Orange Cap (Most Runs)
        top_scorer = "N/A"
        top_scorer_runs = 0
        if 'batter' in filtered_deliveries.columns and 'runs_batter' in filtered_deliveries.columns:
            # Ensure runs are numeric
            filtered_deliveries['runs_batter'] = pd.to_numeric(filtered_deliveries['runs_batter'], errors='coerce').fillna(0)
            batsman_runs = filtered_deliveries.groupby('batter')['runs_batter'].sum().sort_values(ascending=False)
            if not batsman_runs.empty:
                top_scorer = str(batsman_runs.index[0])
                top_scorer_runs = int(batsman_runs.iloc[0])

        # Purple Cap (Most Wickets)
        top_wicket_taker = "N/A"
        top_wickets = 0
        valid_wickets = ['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
        if 'bowler' in filtered_deliveries.columns and 'wicket_kind' in filtered_deliveries.columns:
            is_wkt_mask = filtered_deliveries['wicket_kind'].astype(str).str.lower().isin(valid_wickets)
            bowler_wickets = filtered_deliveries[is_wkt_mask].groupby('bowler').size().sort_values(ascending=False)
            if not bowler_wickets.empty:
                top_wicket_taker = str(bowler_wickets.index[0])
                top_wickets = int(bowler_wickets.iloc[0])

        # MVP / Player of Match
        top_mvp = "N/A"
        top_mvp_awards = 0
        if 'player_of_match' in filtered_matches.columns:
            mvps = filtered_matches['player_of_match'].value_counts()
            if "Unknown" in mvps: mvps = mvps.drop("Unknown")
            if not mvps.empty:
                top_mvp = str(mvps.index[0])
                top_mvp_awards = int(mvps.iloc[0])

        # Metrics Row
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Matches Played", total_matches)
        m2.metric("👑 Orange Cap", top_scorer, f"↑ {top_scorer_runs} Runs")
        m3.metric("🎯 Purple Cap", top_wicket_taker, f"↑ {top_wickets} Wickets")
        m4.metric("⭐ Most MVP", top_mvp, f"↑ {top_mvp_awards} Awards")
        
        st.markdown("---")

        col_left, col_right = st.columns([1.4, 1])

        with col_left:
            st.subheader("🥇 IPL All-Time Champions")
            history_data = {
                'Team': ['Chennai Super Kings', 'Mumbai Indians', 'Kolkata Knight Riders', 'Royal Challengers Bengaluru', 'Sunrisers Hyderabad', 'Gujarat Titans', 'Rajasthan Royals', 'Deccan Chargers'],
                'Titles Won': [5, 5, 3, 1, 1, 1, 1, 1],
                'Winning Years': ['2010, 2011, 2018, 2021, 2023', '2013, 2015, 2017, 2019, 2020', '2012, 2014, 2024', '2025', '2016', '2022', '2008', '2009']
            }
            st.dataframe(pd.DataFrame(history_data), use_container_width=True, hide_index=True)
            
            st.subheader("🏁 Match Performance Breakdown")
            if 'batting_team' in filtered_matches.columns and 'bowling_team' in filtered_matches.columns and 'match_won_by' in filtered_matches.columns:
                all_teams = pd.concat([filtered_matches['batting_team'], filtered_matches['bowling_team']]).dropna().unique()
                points_data = []
                for team in all_teams:
                    played = len(filtered_matches[(filtered_matches['batting_team'] == team) | (filtered_matches['bowling_team'] == team)])
                    wins = len(filtered_matches[filtered_matches['match_won_by'] == team])
                    points_data.append({'Team': team, 'M': played, 'W': wins})
                if points_data:
                    st.dataframe(pd.DataFrame(points_data).sort_values(by='W', ascending=False), use_container_width=True, height=250)

        with col_right:
            st.subheader("🏏 Top 10 Run Scorers")
            if 'batter' in filtered_deliveries.columns and 'runs_batter' in filtered_deliveries.columns:
                try:
                    top_batsmen = filtered_deliveries.groupby('batter')['runs_batter'].sum().sort_values(ascending=False).head(10)
                    st.bar_chart(top_batsmen, color="#FF8C00", height=220)
                except Exception:
                    st.warning("Could not generate Run Scorer chart.")

            st.subheader("🎯 Top 10 Wicket Takers")
            if 'bowler' in filtered_deliveries.columns and 'wicket_kind' in filtered_deliveries.columns:
                try:
                    is_wkt_mask = filtered_deliveries['wicket_kind'].astype(str).str.lower().isin(valid_wickets)
                    top_bowlers = filtered_deliveries[is_wkt_mask].groupby('bowler').size().sort_values(ascending=False).head(10)
                    st.bar_chart(top_bowlers, color="#8A2BE2", height=220)
                except Exception:
                    st.warning("Could not generate Wicket Taker chart.")

    # ==========================================
    # TAB 2: MATCH SCORECARD INSPECTOR
    # ==========================================
    with tab2:
        st.subheader("🔍 Select an IPL Match to Inspect")
        
        if 'date' in filtered_matches.columns and 'batting_team' in filtered_matches.columns and 'bowling_team' in filtered_matches.columns:
            display_matches = filtered_matches.copy()
            # Attempt to safely parse dates, ignoring weird formats
            display_matches['date'] = pd.to_datetime(display_matches['date'], format='mixed', errors='coerce')
            display_matches = display_matches.sort_values(by='date', ascending=False)
            
            # Create a display string
            display_matches['display_name'] = display_matches['date'].dt.strftime('%Y-%m-%d').fillna('Unknown Date') + " | " + display_matches['batting_team'].astype(str) + " vs " + display_matches['bowling_team'].astype(str)
            
            selected_match_str = st.selectbox("Choose Match", display_matches['display_name'].dropna().tolist(), label_visibility="collapsed")
            
            if selected_match_str:
                target_match = display_matches[display_matches['display_name'] == selected_match_str].iloc[0]
                target_match_id = target_match['match_id'] if 'match_id' in target_match else None
                
                venue = target_match['venue'] if 'venue' in target_match else "Unknown Venue"
                winner = target_match['match_won_by'] if 'match_won_by' in target_match else "Unknown"
                pom = target_match['player_of_match'] if 'player_of_match' in target_match else "Unknown"
                
                st.success(f"🏟️ **Venue:** {venue}  |  🏆 **Winner:** {winner}  |  ⭐ **Player of the Match:** {pom}")
                
                if target_match_id is not None and not filtered_deliveries.empty and 'match_id' in filtered_deliveries.columns:
                    m_balls = filtered_deliveries[filtered_deliveries['match_id'] == target_match_id].copy()
                    
                    if not m_balls.empty and 'innings' in m_balls.columns:
                        for innings_num in sorted(m_balls['innings'].dropna().unique()):
                            inn_df = m_balls[m_balls['innings'] == innings_num]
                            
                            bat_team = inn_df['batting_team'].iloc[0] if 'batting_team' in inn_df.columns else f"Innings {innings_num}"
                            st.markdown(f"### 🏏 Innings {int(innings_num)}: {bat_team}")
                            
                            if 'batter' in inn_df.columns and 'runs_batter' in inn_df.columns:
                                bat_card = inn_df.groupby('batter').agg(Runs=('runs_batter', 'sum'), Balls=('runs_batter', 'count'))
                                st.dataframe(bat_card.sort_values(by='Runs', ascending=False), use_container_width=True)
                            
                            if 'bowler' in inn_df.columns and 'runs_batter' in inn_df.columns and 'wicket_kind' in inn_df.columns:
                                bowl_card = inn_df.groupby('bowler').agg(
                                    Wickets=('wicket_kind', lambda x: x.astype(str).str.lower().isin(valid_wickets).sum()),
                                    Runs=('runs_batter', 'sum') # Simplified runs calculation
                                )
                                st.dataframe(bowl_card.sort_values(by='Wickets', ascending=False), use_container_width=True)
                            st.markdown("---")
                    else:
                        st.info("Ball-by-ball details not available for this specific match.")
                else:
                    st.info("Could not link match to delivery records.")
        else:
            st.warning("Match details (date, teams) missing from the dataset. Cannot build inspector.")