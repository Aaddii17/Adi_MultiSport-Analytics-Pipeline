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
    Loads historical IPL data and merges it dynamically with the new 2026 data.
    Ensures all-time stats are automatically updated.
    """
    # 1. Initialize empty DataFrames
    df_history_matches = pd.DataFrame()
    df_history_deliveries = pd.DataFrame()
    df_2026_matches = pd.DataFrame()
    df_2026_deliveries = pd.DataFrame()

    # 2. Load Historical Data (Adjust these paths to where your historical data lives)
    try:
        df_history_matches = pd.read_csv("Data/historical_matches.csv")
        df_history_deliveries = pd.read_csv("Data/historical_deliveries.csv")
    except FileNotFoundError:
        pass # It's okay if it's missing while testing, it will just load 2026

    # 3. Load 2026 Data from the new folder
    try:
        df_2026_matches = pd.read_csv("Data/IPL_2026/matches.csv")
        df_2026_deliveries = pd.read_csv("Data/IPL_2026/deliveries.csv")
        
        # Ensure the 'season' column exists and is set to 2026 so the dropdown works
        if 'season' not in df_2026_matches.columns:
            df_2026_matches['season'] = 2026
        if 'season' not in df_2026_deliveries.columns:
            df_2026_deliveries['season'] = 2026
    except FileNotFoundError:
        st.warning("⚠️ Could not find 'Data/IPL_2026/matches.csv'. Please ensure the folder is named correctly.")

    # 4. Merge them together seamlessly
    all_matches = pd.concat([df_history_matches, df_2026_matches], ignore_index=True)
    all_deliveries = pd.concat([df_history_deliveries, df_2026_deliveries], ignore_index=True)

    return all_matches, all_deliveries

# ==========================================
# MAIN DASHBOARD FUNCTION
# ==========================================
def run_ipl_analysis():
    st.header("🏏 IPL Analytics Hub")
    
    # Load the merged data
    matches, deliveries = load_and_merge_ipl_data()
    
    if matches.empty:
        st.error("No IPL data available. Please check your Data folder.")
        return

    # --- SEASON DROPDOWN ---
    # Automatically extracts unique seasons (e.g., 2026, 2025, 2024...) and adds "All-Time"
    season_list = sorted(matches['season'].dropna().unique().tolist(), reverse=True)
    seasons = ["All-Time"] + [str(int(s)) for s in season_list]
    
    selected_season = st.selectbox("📅 Select IPL Season:", seasons)

    # --- DATA FILTERING ---
    if selected_season != "All-Time":
        filtered_matches = matches[matches['season'] == int(selected_season)]
        # We merge deliveries with matches to filter deliveries by season
        if not deliveries.empty and 'match_id' in deliveries.columns and 'id' in filtered_matches.columns:
            filtered_deliveries = deliveries[deliveries['match_id'].isin(filtered_matches['id'])]
        else:
            filtered_deliveries = deliveries # Fallback
    else:
        filtered_matches = matches
        filtered_deliveries = deliveries

    # --- TABS ---
    tab1, tab2 = st.tabs(["📊 Tournament Leaderboard & History", "🔍 Match Scorecard Inspector"])

    with tab1:
        # --- TOP METRICS ---
        col1, col2, col3, col4 = st.columns(4)
        
        matches_played = len(filtered_matches)
        
        # Calculate Orange Cap (Most Runs)
        orange_cap_player = "N/A"
        orange_cap_runs = 0
        if not filtered_deliveries.empty and 'batsman' in filtered_deliveries.columns and 'batsman_runs' in filtered_deliveries.columns:
            run_scorers = filtered_deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False)
            if not run_scorers.empty:
                orange_cap_player = run_scorers.index[0]
                orange_cap_runs = run_scorers.iloc[0]

        # Calculate Purple Cap (Most Wickets)
        purple_cap_player = "N/A"
        purple_cap_wickets = 0
        if not filtered_deliveries.empty and 'bowler' in filtered_deliveries.columns and 'is_wicket' in filtered_deliveries.columns:
            # Note: You may need to filter 'dismissal_kind' to exclude run outs based on your exact CSV structure
            wicket_takers = filtered_deliveries.groupby('bowler')['is_wicket'].sum().sort_values(ascending=False)
            if not wicket_takers.empty:
                purple_cap_player = wicket_takers.index[0]
                purple_cap_wickets = wicket_takers.iloc[0]

        # MVP / Player of Match
        mvp_player = "N/A"
        mvp_awards = 0
        if 'player_of_match' in filtered_matches.columns:
            mvps = filtered_matches['player_of_match'].value_counts()
            if not mvps.empty:
                mvp_player = mvps.index[0]
                mvp_awards = mvps.iloc[0]

        with col1:
            st.metric("Matches Played", matches_played)
        with col2:
            st.metric("👑 Orange Cap", orange_cap_player, f"↑ {orange_cap_runs} Runs")
        with col3:
            st.metric("🎯 Purple Cap", purple_cap_player, f"↑ {purple_cap_wickets} Wickets")
        with col4:
            st.metric("⭐ Most MVP", mvp_player, f"↑ {mvp_awards} Awards")

        st.markdown("---")

        # --- CHARTS AND TABLES ---
        col_left, col_right = st.columns([1, 1])

        with col_left:
            st.markdown("### 🥇 IPL Champions / Winners")
            if 'winner' in filtered_matches.columns:
                wins = filtered_matches['winner'].value_counts().reset_index()
                wins.columns = ['Team', 'Matches Won']
                st.dataframe(wins, use_container_width=True, hide_index=True)

        with col_right:
            st.markdown("### 🏏 Top 10 Run Scorers")
            if not filtered_deliveries.empty and 'batsman' in filtered_deliveries.columns:
                top_batsmen = filtered_deliveries.groupby('batsman')['batsman_runs'].sum().sort_values(ascending=False).head(10).reset_index()
                fig_bat = px.bar(top_batsmen, x='batsman', y='batsman_runs', color_discrete_sequence=['#ff9900'])
                fig_bat.update_layout(xaxis_title="", yaxis_title="Runs", margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig_bat, use_container_width=True)

            st.markdown("### 🎯 Top 10 Wicket Takers")
            if not filtered_deliveries.empty and 'bowler' in filtered_deliveries.columns:
                top_bowlers = filtered_deliveries.groupby('bowler')['is_wicket'].sum().sort_values(ascending=False).head(10).reset_index()
                fig_bowl = px.bar(top_bowlers, x='bowler', y='is_wicket', color_discrete_sequence=['#8a2be2'])
                fig_bowl.update_layout(xaxis_title="", yaxis_title="Wickets", margin=dict(l=0, r=0, t=0, b=0))
                st.plotly_chart(fig_bowl, use_container_width=True)

    with tab2:
        st.markdown("### 🔍 Select an IPL Match to Inspect")
        st.info("Match Scorecard Inspector logic goes here. (Select a specific match from the filtered matches to view detailed innings).")
        # You can add your specific scorecard inspector logic here!