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
    Loads historical IPL data (Parquet) and merges it dynamically with the new 2026 CSV data.
    Translates Kaggle columns to match the historical Parquet format perfectly.
    """
    df_history_matches = pd.DataFrame()
    df_history_deliveries = pd.DataFrame()
    df_2026_matches = pd.DataFrame()
    df_2026_deliveries = pd.DataFrame()

    # 1. Load User's Historical Parquet File
    parquet_path = "data/ipl_ball_by_ball_2008_2025.parquet"
    if os.path.exists(parquet_path):
        hist_df = pd.read_parquet(parquet_path)
        df_history_deliveries = hist_df
        if 'match_id' in hist_df.columns:
            df_history_matches = hist_df.drop_duplicates(subset=['match_id']).copy()
    else:
        # Fallback to standard CSVs if parquet is missing
        history_dir = "data" if os.path.exists("data/historical_matches.csv") else "Data"
        try:
            df_history_matches = pd.read_csv(f"{history_dir}/historical_matches.csv")
            df_history_deliveries = pd.read_csv(f"{history_dir}/historical_deliveries.csv")
        except FileNotFoundError:
            pass 

    # 2. Load 2026 Kaggle Data and Standardize Columns
    ipl_2026_dir = "data/IPL_2026" if os.path.exists("data/IPL_2026/matches.csv") else "Data/IPL_2026"
    try:
        df_2026_matches = pd.read_csv(f"{ipl_2026_dir}/matches.csv")
        df_2026_deliveries = pd.read_csv(f"{ipl_2026_dir}/deliveries.csv")
        
        # Translate 2026 Match Columns to match the historical format
        match_mapping = {
            'id': 'match_id',
            'match_winner': 'match_won_by',
            'team1': 'batting_team',
            'team2': 'bowling_team'
        }
        df_2026_matches.rename(columns=match_mapping, inplace=True)
        
        # Translate 2026 Delivery Columns to match the historical format
        delivery_mapping = {
            'match_no': 'match_id',
            'striker': 'batter',
            'runs_of_bat': 'runs_batter',
            'wicket_type': 'wicket_kind'
        }
        df_2026_deliveries.rename(columns=delivery_mapping, inplace=True)

        # Ensure seasons are set
        if 'season' not in df_2026_matches.columns:
            df_2026_matches['season'] = '2026'
        if 'season' not in df_2026_deliveries.columns:
            df_2026_deliveries['season'] = '2026'
            
    except FileNotFoundError:
        st.warning(f"⚠️ Could not find '{ipl_2026_dir}/matches.csv'. Please ensure the folder is pushed to GitHub.")

    # 3. Merge Datasets Seamlessly
    all_matches = pd.concat([df_history_matches, df_2026_matches], ignore_index=True)
    all_deliveries = pd.concat([df_history_deliveries, df_2026_deliveries], ignore_index=True)

    return all_matches, all_deliveries

# ==========================================
# MAIN DASHBOARD FUNCTION
# ==========================================
def run_ipl_analysis():
    st.header("🏏 IPL Analytics Hub")
    st.markdown("---")
    
    with st.spinner("Analyzing IPL historical records and merging 2026 data..."):
        matches, deliveries = load_and_merge_ipl_data()
    
    if matches.empty:
        st.error("No IPL data available. Please check your Data folder.")
        return

    # --- CLEAN & FORMAT SEASON DROPDOWN ---
    if 'season' in matches.columns:
        matches['season'] = matches['season'].astype(str).str.replace(r'\.0$', '', regex=True)
        season_list = sorted(matches['season'].dropna().unique().tolist(), reverse=True)
    else:
        season_list = []
        
    seasons = ["All-Time"] + season_list
    st.write("🗓️ **Select IPL Season:**")
    selected_season = st.selectbox("Season Dropdown", seasons, label_visibility="collapsed", key="ipl_season")

    # --- DYNAMIC COLUMN ASSIGNMENTS (Crash Prevention) ---
    m_id = 'match_id' if 'match_id' in matches.columns else 'id'
    m_winner = 'match_won_by' if 'match_won_by' in matches.columns else 'winner'
    m_pom = 'player_of_match'
    d_id = 'match_id' if 'match_id' in deliveries.columns else 'match_no'
    d_batter = 'batter' if 'batter' in deliveries.columns else 'batsman'
    d_runs = 'runs_batter' if 'runs_batter' in deliveries.columns else 'batsman_runs'
    d_wicket = 'wicket_kind' if 'wicket_kind' in deliveries.columns else 'dismissal_kind'

    # --- FILTER BY SEASON ---
    if selected_season != "All-Time":
        filtered_matches = matches[matches['season'] == selected_season]
        if not deliveries.empty and d_id in deliveries.columns and m_id in filtered_matches.columns:
            filtered_deliveries = deliveries[deliveries[d_id].isin(filtered_matches[m_id])]
        else:
            filtered_deliveries = deliveries 
    else:
        filtered_matches = matches
        filtered_deliveries = deliveries

    valid_wickets = ['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']

    tab1, tab2 = st.tabs(["📊 Tournament Leaderboard & History", "🔍 Match Scorecard Inspector"])

    # ==========================================
    # TAB 1: TOURNAMENT STATS & CHAMPIONS
    # ==========================================
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        matches_played = filtered_matches[m_id].nunique() if m_id in filtered_matches.columns else len(filtered_matches)
        
        # Orange Cap
        orange_cap_player, orange_cap_runs = "N/A", 0
        if d_batter in filtered_deliveries.columns and d_runs in filtered_deliveries.columns:
            run_scorers = filtered_deliveries.groupby(d_batter)[d_runs].sum().sort_values(ascending=False)
            if not run_scorers.empty:
                orange_cap_player, orange_cap_runs = str(run_scorers.index[0]), int(run_scorers.iloc[0])

        # Purple Cap
        purple_cap_player, purple_cap_wickets = "N/A", 0
        if 'bowler' in filtered_deliveries.columns and d_wicket in filtered_deliveries.columns:
            is_wkt_mask = filtered_deliveries[d_wicket].astype(str).str.lower().isin(valid_wickets)
            wicket_takers = filtered_deliveries[is_wkt_mask].groupby('bowler').size().sort_values(ascending=False)
            if not wicket_takers.empty:
                purple_cap_player, purple_cap_wickets = str(wicket_takers.index[0]), int(wicket_takers.iloc[0])

        # MVP
        mvp_player, mvp_awards = "N/A", 0
        if m_pom in filtered_matches.columns:
            mvps = filtered_matches[m_pom].value_counts()
            if "Unknown" in mvps: mvps = mvps.drop("Unknown")
            if not mvps.empty:
                mvp_player, mvp_awards = str(mvps.index[0]), int(mvps.iloc[0])

        col1.metric("Matches Played", matches_played)
        col2.metric("👑 Orange Cap", orange_cap_player, f"↑ {orange_cap_runs} Runs")
        col3.metric("🎯 Purple Cap", purple_cap_player, f"↑ {purple_cap_wickets} Wickets")
        col4.metric("⭐ Most MVP", mvp_player, f"↑ {mvp_awards} Awards")
        
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
            if 'batting_team' in filtered_matches.columns and 'bowling_team' in filtered_matches.columns and m_winner in filtered_matches.columns:
                all_teams = pd.concat([filtered_matches['batting_team'], filtered_matches['bowling_team']]).dropna().unique()
                points_data = []
                for team in all_teams:
                    played = len(filtered_matches[(filtered_matches['batting_team'] == team) | (filtered_matches['bowling_team'] == team)])
                    wins = len(filtered_matches[filtered_matches[m_winner] == team])
                    points_data.append({'Team': team, 'M': played, 'W': wins})
                if points_data:
                    st.dataframe(pd.DataFrame(points_data).sort_values(by='W', ascending=False), use_container_width=True, height=250)

        with col_right:
            st.subheader("🏏 Top 10 Run Scorers")
            if d_batter in filtered_deliveries.columns and d_runs in filtered_deliveries.columns:
                top_batsmen = filtered_deliveries.groupby(d_batter)[d_runs].sum().sort_values(ascending=False).head(10).reset_index()
                fig_bat = px.bar(top_batsmen, x=d_batter, y=d_runs, color_discrete_sequence=['#FF8C00'])
                fig_bat.update_layout(xaxis_title="", yaxis_title="Runs", margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig_bat, use_container_width=True)

            st.subheader("🎯 Top 10 Wicket Takers")
            if 'bowler' in filtered_deliveries.columns and d_wicket in filtered_deliveries.columns:
                is_wkt_mask = filtered_deliveries[d_wicket].astype(str).str.lower().isin(valid_wickets)
                top_bowlers = filtered_deliveries[is_wkt_mask].groupby('bowler').size().sort_values(ascending=False).head(10).reset_index(name='Wickets')
                fig_bowl = px.bar(top_bowlers, x='bowler', y='Wickets', color_discrete_sequence=['#8A2BE2'])
                fig_bowl.update_layout(xaxis_title="", yaxis_title="Wickets", margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig_bowl, use_container_width=True)

    # ==========================================
    # TAB 2: MATCH SCORECARD INSPECTOR
    # ==========================================
    with tab2:
        st.subheader("🔍 Select an IPL Match to Inspect")
        
        if 'date' in filtered_matches.columns and 'batting_team' in filtered_matches.columns and 'bowling_team' in filtered_matches.columns:
            display_matches = filtered_matches.copy()
            display_matches['date'] = pd.to_datetime(display_matches['date'], errors='coerce')
            display_matches = display_matches.sort_values(by='date', ascending=False)
            display_matches['display_name'] = display_matches['date'].dt.strftime('%Y-%m-%d') + " | " + display_matches['batting_team'].astype(str) + " vs " + display_matches['bowling_team'].astype(str)
            
            selected_match_str = st.selectbox("Choose Match", display_matches['display_name'].dropna().tolist(), label_visibility="collapsed")
            
            if selected_match_str:
                target_match = display_matches[display_matches['display_name'] == selected_match_str].iloc[0]
                target_match_id = target_match[m_id]
                
                venue = target_match['venue'] if 'venue' in target_match else "Unknown Venue"
                winner = target_match[m_winner] if m_winner in target_match else "Unknown"
                pom = target_match[m_pom] if m_pom in target_match else "Unknown"
                
                st.success(f"🏟️ **Venue:** {venue}  |  🏆 **Winner:** {winner}  |  ⭐ **Player of the Match:** {pom}")
                
                m_balls = filtered_deliveries[filtered_deliveries[d_id] == target_match_id].copy()
                
                if not m_balls.empty and 'innings' in m_balls.columns:
                    for innings_num in sorted(m_balls['innings'].dropna().unique()):
                        inn_df = m_balls[m_balls['innings'] == innings_num]
                        
                        bat_team = inn_df['batting_team'].iloc[0] if 'batting_team' in inn_df.columns else f"Innings {innings_num}"
                        st.markdown(f"### 🏏 Innings {int(innings_num)}: {bat_team}")
                        
                        if d_batter in inn_df.columns and d_runs in inn_df.columns:
                            bat_card = inn_df.groupby(d_batter).agg(Runs=(d_runs, 'sum'), Balls=(d_runs, 'count'))
                            st.dataframe(bat_card.sort_values(by='Runs', ascending=False), use_container_width=True)
                        
                        if 'bowler' in inn_df.columns and d_runs in inn_df.columns:
                            bowl_card = inn_df.groupby('bowler').agg(
                                Wickets=(d_wicket, lambda x: x.astype(str).str.lower().isin(valid_wickets).sum() if d_wicket in inn_df.columns else 0),
                                Runs=(d_runs, 'sum')
                            )
                            st.dataframe(bowl_card.sort_values(by='Wickets', ascending=False), use_container_width=True)
                        st.markdown("---")
                else:
                    st.info("Ball-by-ball details not available for this specific match.")
        else:
            st.warning("Match details (date, teams) missing from the dataset. Cannot build inspector.")