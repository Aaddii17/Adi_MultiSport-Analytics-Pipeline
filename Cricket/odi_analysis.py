import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # Safely route to the new Parquet file
    data_path = "data/odi_combined.parquet" if os.path.exists("data/odi_combined.parquet") else "../data/odi_combined.parquet"
    
    try:
        df = pd.read_parquet(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading ODI data: {e}")
        return pd.DataFrame()

def run_odi_analysis():
    st.header("🌍 Men's One Day International (ODI) Hub")
    st.markdown("---")
    
    with st.spinner("Loading decades of ODI history..."):
        df = load_data()
        
    st.write("🗓️ **Select Calendar Year:**")
    years = sorted(df['year'].dropna().unique().tolist(), reverse=True)
    if "All-Time" not in years:
        years.insert(0, "All-Time")
        
    selected_year = st.selectbox("Year Dropdown", years, label_visibility="collapsed", key="odi_year")
    
    if selected_year != "All-Time":
        filtered_df = df[df['year'] == selected_year]
    else:
        filtered_df = df
        
    match_level_df = filtered_df.drop_duplicates(subset=['match_id']).copy()
    
    tab1, tab2 = st.tabs(["📊 Global Leaderboard", "🔍 Match Scorecard Inspector"])
    
    # ==========================================
    # TAB 1: TOURNAMENT STATS
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
        m2.metric("👑 Most Runs", f"{top_scorer}", f"{top_scorer_runs} Runs")
        m3.metric("🎯 Most Wickets", f"{top_wicket_taker}", f"{top_wickets} Wickets")
        m4.metric("⭐ Most MVPs", f"{top_mvp}", f"{top_mvp_awards} Awards")
        
        st.markdown("---")
        col_table, col_charts = st.columns([1.4, 1])
        
        with col_table:
            st.subheader("🏁 Global Win Summary")
            all_teams = pd.concat([match_level_df['batting_team'], match_level_df['bowling_team']]).dropna().unique()
            
            points_data = []
            for team in all_teams:
                played = len(match_level_df[(match_level_df['batting_team'] == team) | (match_level_df['bowling_team'] == team)])
                wins = len(match_level_df[match_level_df['match_won_by'] == team])
                losses = len(match_level_df[((match_level_df['batting_team'] == team) | (match_level_df['bowling_team'] == team)) & (match_level_df['match_won_by'].notna()) & (match_level_df['match_won_by'] != team)])
                nr_tie = played - wins - losses
                win_pct = round((wins / played) * 100, 1) if played > 0 else 0.0
                points_data.append({'Team': team, 'P': played, 'W': wins, 'L': losses, 'NR/Tie': nr_tie, 'Win %': win_pct})
                
            if points_data:
                points_df = pd.DataFrame(points_data).sort_values(by=['W', 'Win %'], ascending=[False, False])
                points_df.index = range(1, len(points_df) + 1)
                st.dataframe(points_df, use_container_width=True, height=480)
            else:
                st.info("No match data available to generate points table.")
            
        with col_charts:
            st.subheader("🏏 Top 10 Batting Performances")
            st.bar_chart(batsman_runs.head(10), color="#1976D2", height=200) # Classic Blue
            
            st.subheader("🎯 Top 10 Bowling Performances")
            st.bar_chart(bowler_wickets.head(10), color="#FF5722", height=200) # Deep Orange

    # ==========================================
    # TAB 2: MATCH SCORECARD INSPECTOR (UPGRADED)
    # ==========================================
    with tab2:
        st.subheader("🔍 Filter & Select an ODI Match")
        
        if not match_level_df.empty:
            # 1. Create Team Filters
            all_teams_filter = sorted(pd.concat([match_level_df['batting_team'], match_level_df['bowling_team']]).dropna().unique().tolist())
            team_options = ["All Teams"] + all_teams_filter
            
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                team1_filter = st.selectbox("Filter by Team 1:", team_options, key="odi_t1")
            with col_f2:
                team2_filter = st.selectbox("Filter by Team 2:", team_options, key="odi_t2")
                
            # 2. Apply Filters to the Dataframe
            filtered_matches = match_level_df.copy()
            if team1_filter != "All Teams":
                filtered_matches = filtered_matches[(filtered_matches['batting_team'] == team1_filter) | (filtered_matches['bowling_team'] == team1_filter)]
            if team2_filter != "All Teams":
                filtered_matches = filtered_matches[(filtered_matches['batting_team'] == team2_filter) | (filtered_matches['bowling_team'] == team2_filter)]
            
            st.markdown("---")
            
            # 3. Display Match Selector based on Filtered Data
            if not filtered_matches.empty:
                filtered_matches = filtered_matches.sort_values(by='date', ascending=False)
                
                date_strings = filtered_matches['date'].dt.strftime('%Y-%m-%d').fillna('Unknown Date')
                filtered_matches['display_name'] = date_strings + " | " + filtered_matches['batting_team'].astype(str) + " vs " + filtered_matches['bowling_team'].astype(str)
                
                selected_match_str = st.selectbox("Choose Match:", filtered_matches['display_name'].tolist(), label_visibility="collapsed", key="odi_match_selector")
                
                if selected_match_str:
                    target_match_id = filtered_matches[filtered_matches['display_name'] == selected_match_str]['match_id'].values[0]
                    m_balls = df[df['match_id'] == target_match_id].copy()
                    m_info = m_balls.iloc[0]
                    
                    st.success(f"🏟️ **Venue:** {m_info['venue']}  |  🏆 **Winner:** {m_info['match_won_by']}  |  ⭐ **Player of the Match:** {m_info['player_of_match']}")
                    
                    for innings_num in sorted(m_balls['innings'].dropna().unique()):
                        inn_df = m_balls[m_balls['innings'] == innings_num]
                        bat_team = inn_df['batting_team'].iloc[0]
                        
                        total_runs = inn_df['runs_batter'].sum() + inn_df['runs_extras'].sum()
                        total_wickets = inn_df['wicket_kind'].dropna().count()
                        
                        st.markdown(f"### 🏏 Innings {int(innings_num)}: {bat_team} - {total_runs}/{total_wickets}")
                        
                        bat_card = inn_df.groupby('batter').agg(
                            Runs=('runs_batter', 'sum'),
                            Balls=('runs_batter', 'count'),
                            Fours=('runs_batter', lambda x: (x == 4).sum()),
                            Sixes=('runs_batter', lambda x: (x == 6).sum())
                        )
                        bat_card['SR'] = round((bat_card['Runs'] / bat_card['Balls']) * 100, 1) if not bat_card.empty else 0.0
                        st.dataframe(bat_card.sort_values(by='Runs', ascending=False), use_container_width=True)
                        
                        bowl_card = inn_df.groupby('bowler').agg(
                            Runs_Conceded=('runs_batter', 'sum'),
                            Balls_Bowled=('runs_batter', 'count'),
                            Wickets=('wicket_kind', lambda x: x.isin(valid_wickets).sum())
                        )
                        bowl_card['Overs'] = bowl_card['Balls_Bowled'] // 6 + (bowl_card['Balls_Bowled'] % 6) / 10
                        bowl_card['Econ'] = round((bowl_card['Runs_Conceded'] / bowl_card['Balls_Bowled']) * 6, 2)
                        
                        st.dataframe(bowl_card[['Overs', 'Runs_Conceded', 'Wickets', 'Econ']].sort_values(by='Wickets', ascending=False), use_container_width=True)
                        st.markdown("---")
            else:
                st.warning("⚠️ No matches found between these selected teams in the chosen year.")
        else:
            st.info("No match records found for this selection.")