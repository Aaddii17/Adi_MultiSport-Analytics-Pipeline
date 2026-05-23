import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    # FIX: We force Pandas to parse the date column correctly right at the source
    df = pd.read_csv("data/odiwc_combined.csv", low_memory=False, parse_dates=['date'])
    return df

def run_odiwc_analysis():
    st.header("🏆 Men's ODI Cricket World Cup Analytics Hub")
    st.markdown("---")
    
    with st.spinner("Analyzing World Cup archives..."):
        df = load_data()
        
    st.write("🗓️ **Select World Cup Edition (Year):**")
    years = sorted(df['year'].dropna().astype(str).unique().tolist(), reverse=True)
    if "All-Time" not in years:
        years.insert(0, "All-Time") 
    selected_year = st.selectbox("Year Dropdown", years, label_visibility="collapsed", key="odiwc_year")
    
    if selected_year != "All-Time":
        filtered_df = df[df['year'].astype(str) == selected_year]
    else:
        filtered_df = df
        
    match_level_df = filtered_df.drop_duplicates(subset=['match_id']).copy()
    
    # Create two primary viewing layouts
    tab1, tab2 = st.tabs(["📊 Tournament Leaderboard", "🔍 Match Scorecard Inspector"])
    
    # ==========================================
    # TAB 1: TOURNAMENT LEVEL STATS
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
        m1.metric("Total Matches", total_matches)
        m2.metric("👑 Golden Bat", f"{top_scorer}", f"{top_scorer_runs} Runs")
        m3.metric("🎯 Golden Ball", f"{top_wicket_taker}", f"{top_wickets} Wickets")
        m4.metric("⭐ Tournament MVPs", f"{top_mvp}", f"{top_mvp_awards} Awards")
        
        st.markdown("---")
        col_table, col_charts = st.columns([1.4, 1])
        
        with col_table:
            # --- HISTORICAL CHAMPIONS LEADERBOARD ---
            st.subheader("🥇 Men's ODI World Cup Champions")
            history_data = {
                'Team': ['Australia', 'India', 'West Indies', 'Pakistan', 'Sri Lanka', 'England'],
                'Titles Won': [6, 2, 2, 1, 1, 1],
                'Winning Years': [
                    '1987, 1999, 2003, 2007, 2015, 2023',
                    '1983, 2011',
                    '1975, 1979',
                    '1992',
                    '1996',
                    '2019'
                ]
            }
            history_df = pd.DataFrame(history_data)
            history_df.index = range(1, len(history_df) + 1)
            st.dataframe(history_df, use_container_width=True)
            st.markdown("---")
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
                
            points_df = pd.DataFrame(points_data).sort_values(by=['W', 'Win %'], ascending=[False, False])
            points_df.index = range(1, len(points_df) + 1)
            st.dataframe(points_df, use_container_width=True, height=480)
            
        with col_charts:
            st.subheader("🏏 Top 10 Batting Performances")
            st.bar_chart(batsman_runs.head(10), color="#008080", height=200) 
            st.subheader("🎯 Top 10 Bowling Performances")
            st.bar_chart(bowler_wickets.head(10), color="#FFD700", height=200) 

    # ==========================================
    # TAB 2: DETAILED MATCH INSPECTOR
    # ==========================================
    with tab2:
        st.subheader("🔍 Select a Match to Inspect")
        
        if not match_level_df.empty:
            # Build clean dropdown string format safely now that date is guaranteed to be parsed
            match_level_df = match_level_df.sort_values(by='date', ascending=False)
            match_level_df['display_name'] = match_level_df['date'].dt.strftime('%Y-%m-%d') + " | " + match_level_df['batting_team'].astype(str) + " vs " + match_level_df['bowling_team'].astype(str)
            
            selected_match_str = st.selectbox("Choose Match", match_level_df['display_name'].tolist(), label_visibility="collapsed")
            
            if selected_match_str:
                target_match_id = match_level_df[match_level_df['display_name'] == selected_match_str]['match_id'].values[0]
                m_balls = df[df['match_id'] == target_match_id]
                m_info = m_balls.iloc[0]
                
                st.success(f"🏟️ **Venue:** {m_info['venue']}  |  🏆 **Winner:** {m_info['match_won_by']}  |  ⭐ **Player of the Match:** {m_info['player_of_match']}")
                
                for innings_num in sorted(m_balls['innings'].unique()):
                    inn_df = m_balls[m_balls['innings'] == innings_num]
                    bat_team = inn_df['batting_team'].iloc[0]
                    
                    total_runs = inn_df['runs_batter'].sum() + inn_df['runs_extras'].sum()
                    total_wickets = inn_df['wicket_kind'].dropna().count()
                    
                    st.markdown(f"### 🏏 Innings {innings_num}: {bat_team} - {total_runs}/{total_wickets}")
                    
                    bat_card = inn_df.groupby('batter').agg(
                        Runs=('runs_batter', 'sum'),
                        Balls=('runs_batter', 'count'),
                        Fours=('runs_batter', lambda x: (x == 4).sum()),
                        Sixes=('runs_batter', lambda x: (x == 6).sum())
                    )
                    bat_card['SR'] = round((bat_card['Runs'] / bat_card['Balls']) * 100, 1)
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
            st.info("No match records found for this selection.")