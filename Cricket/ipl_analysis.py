import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Loading your specific NTCC dataset
    df = pd.read_parquet("data/ipl_ball_by_ball_2008_2025.parquet")
    df['date'] = pd.to_datetime(df['date'], format='mixed', errors='coerce')
    return df

def run_ipl_analysis():
    st.header("🏏 IPL Analytics Hub")
    st.markdown("---")
    
    with st.spinner("Analyzing IPL historical records..."):
        df = load_data()
        
    df['season'] = df['season'].astype(str)
    
    st.write("🗓️ **Select IPL Season:**")
    seasons = sorted(df['season'].unique().tolist(), reverse=True)
    if "All-Time" not in seasons:
        seasons.insert(0, "All-Time")
        
    selected_season = st.selectbox("Season Dropdown", seasons, label_visibility="collapsed", key="ipl_season")
    
    if selected_season != "All-Time":
        filtered_df = df[df['season'] == selected_season]
    else:
        filtered_df = df
        
    match_level_df = filtered_df.drop_duplicates(subset=['match_id']).copy()
    
    tab1, tab2 = st.tabs(["📊 Tournament Leaderboard & History", "🔍 Match Scorecard Inspector"])
    
    # ==========================================
    # TAB 1: TOURNAMENT STATS & CHAMPIONS
    # ==========================================
    with tab1:
        total_matches = match_level_df['match_id'].nunique()
        
        batsman_runs = filtered_df.groupby('batter')['runs_batter'].sum().sort_values(ascending=False)
        top_scorer = batsman_runs.index[0] if not batsman_runs.empty else "-"
        top_scorer_runs = int(batsman_runs.iloc[0]) if not batsman_runs.empty else 0
        
        valid_wickets = ['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
        bowler_wickets = filtered_df[filtered_df['wicket_kind'].isin(valid_wickets)].groupby('bowler')['player_out'].count().sort_values(ascending=False)
        top_wicket_taker = bowler_wickets.index[0] if not bowler_wickets.empty else "-"
        top_wickets = int(bowler_wickets.iloc[0]) if not bowler_wickets.empty else 0
        
        mvp_counts = match_level_df['player_of_match'].value_counts()
        if "Unknown" in mvp_counts: mvp_counts = mvp_counts.drop("Unknown")
        top_mvp = mvp_counts.index[0] if not mvp_counts.empty else "-"
        top_mvp_awards = int(mvp_counts.iloc[0]) if not mvp_counts.empty else 0
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Matches Played", total_matches)
        m2.metric("👑 Orange Cap", f"{top_scorer}", f"↑ {top_scorer_runs} Runs")
        m3.metric("🎯 Purple Cap", f"{top_wicket_taker}", f"↑ {top_wickets} Wickets")
        m4.metric("⭐ Most MVP", f"{top_mvp}", f"↑ {top_mvp_awards} Awards")
        
        st.markdown("---")
        col_table, col_charts = st.columns([1.4, 1])
        
        with col_table:
            st.subheader("🥇 IPL All-Time Champions")
            history_data = {
                'Team': ['Chennai Super Kings', 'Mumbai Indians', 'Kolkata Knight Riders', 'Royal Challengers Bengaluru', 'Sunrisers Hyderabad', 'Gujarat Titans', 'Rajasthan Royals', 'Deccan Chargers'],
                'Titles Won': [5, 5, 3, 1, 1, 1, 1, 1],
                'Winning Years': ['2010, 2011, 2018, 2021, 2023', '2013, 2015, 2017, 2019, 2020', '2012, 2014, 2024', '2025', '2016', '2022', '2008', '2009']
            }
            st.dataframe(pd.DataFrame(history_data), use_container_width=True)
            
            st.subheader("🏁 Match Performance Breakdown")
            all_teams = pd.concat([match_level_df['batting_team'], match_level_df['bowling_team']]).dropna().unique()
            points_data = []
            for team in all_teams:
                played = len(match_level_df[(match_level_df['batting_team'] == team) | (match_level_df['bowling_team'] == team)])
                wins = len(match_level_df[match_level_df['match_won_by'] == team])
                points_data.append({'Team': team, 'M': played, 'W': wins})
            
            if points_data:
                st.dataframe(pd.DataFrame(points_data).sort_values(by='W', ascending=False), use_container_width=True, height=250)
            
        with col_charts:
            st.subheader("🏏 Top 10 Run Scorers")
            st.bar_chart(batsman_runs.head(10), color="#FF8C00", height=220)
            st.subheader("🎯 Top 10 Wicket Takers")
            st.bar_chart(bowler_wickets.head(10), color="#8A2BE2", height=220)

    # ==========================================
    # TAB 2: MATCH SCORECARD INSPECTOR
    # ==========================================
    with tab2:
        st.subheader("🔍 Select an IPL Match to Inspect")
        match_level_df = match_level_df.sort_values(by='date', ascending=False)
        match_level_df['display_name'] = match_level_df['date'].dt.strftime('%Y-%m-%d') + " | " + match_level_df['batting_team'] + " vs " + match_level_df['bowling_team']
        
        selected_match_str = st.selectbox("Choose Match", match_level_df['display_name'].tolist(), label_visibility="collapsed")
        
        if selected_match_str:
            target_match_id = match_level_df[match_level_df['display_name'] == selected_match_str]['match_id'].values[0]
            m_balls = df[df['match_id'] == target_match_id].copy()
            m_info = m_balls.iloc[0]
            
            st.success(f"🏟️ **Venue:** {m_info['venue']}  |  🏆 **Winner:** {m_info['match_won_by']}  |  ⭐ **Player of the Match:** {m_info['player_of_match']}")
            
            for innings_num in sorted(m_balls['innings'].unique()):
                inn_df = m_balls[m_balls['innings'] == innings_num]
                st.markdown(f"### 🏏 Innings {int(innings_num)}: {inn_df['batting_team'].iloc[0]}")
                
                bat_card = inn_df.groupby('batter').agg(Runs=('runs_batter', 'sum'), Balls=('runs_batter', 'count'))
                st.dataframe(bat_card.sort_values(by='Runs', ascending=False), use_container_width=True)
                
                bowl_card = inn_df.groupby('bowler').agg(Wickets=('wicket_kind', lambda x: x.isin(valid_wickets).sum()), Runs=('runs_batter', 'sum'))
                st.dataframe(bowl_card.sort_values(by='Wickets', ascending=False), use_container_width=True)
                st.markdown("---")