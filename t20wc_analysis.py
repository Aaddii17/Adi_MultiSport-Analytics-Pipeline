import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("data/t20wc_combined.csv", low_memory=False)
    return df

def run_t20wc_analysis():
    st.header("🏆 Men's T20 World Cup Analytics Hub")
    st.markdown("---")
    
    with st.spinner("Loading World Cup history..."):
        df = load_data()
    
    # ==========================================
    # TOURNAMENT FILTER
    # ==========================================
    st.write("🗓️ **Select World Cup Edition (Year):**")
    years = sorted(df['year'].dropna().astype(str).unique().tolist(), reverse=True)
    if "All-Time" not in years:
        years.insert(0, "All-Time") 
    
    selected_year = st.selectbox("Year Dropdown", years, label_visibility="collapsed", key="t20wc_year")
    
    if selected_year != "All-Time":
        filtered_df = df[df['year'].astype(str) == selected_year]
    else:
        filtered_df = df
        
    match_level_df = filtered_df.drop_duplicates(subset=['match_id'])
    
    # ==========================================
    # TOP LEVEL METRICS
    # ==========================================
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
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Tournament Matches", total_matches)
    col2.metric("👑 Most Runs", f"{top_scorer}", f"↑ {top_scorer_runs} Runs")
    col3.metric("🎯 Most Wickets", f"{top_wicket_taker}", f"↑ {top_wickets} Wickets")
    col4.metric("⭐ Most MVP", f"{top_mvp}", f"↑ {top_mvp_awards} Awards")
    
    st.markdown("---")

    # ==========================================
    # SPLIT LAYOUT: TOURNAMENT STANDINGS & CHARTS
    # ==========================================
    col_table, col_charts = st.columns([1.5, 1]) 
    
    with col_table:
        st.subheader("📊 Tournament Performance")
        all_teams = pd.concat([match_level_df['batting_team'], match_level_df['bowling_team']]).dropna().unique()
        
        points_data = []
        for team in all_teams:
            played = len(match_level_df[(match_level_df['batting_team'] == team) | (match_level_df['bowling_team'] == team)])
            wins = len(match_level_df[match_level_df['match_won_by'] == team])
            losses = len(match_level_df[((match_level_df['batting_team'] == team) | (match_level_df['bowling_team'] == team)) & 
                                        (match_level_df['match_won_by'].notna()) & 
                                        (match_level_df['match_won_by'] != team)])
            nr_tie = played - wins - losses
            win_pct = round((wins / played) * 100, 1) if played > 0 else 0.0
            
            points_data.append({'Team': team, 'M': played, 'W': wins, 'L': losses, 'NR/Tie': nr_tie, 'Win %': win_pct})
            
        points_df = pd.DataFrame(points_data).sort_values(by=['W', 'Win %'], ascending=[False, False])
        points_df.index = range(1, len(points_df) + 1)
        st.dataframe(points_df, use_container_width=True, height=520)
        
    with col_charts:
        st.subheader("🏏 Top 10 Run Scorers")
        top_10_bat = batsman_runs.head(10)
        st.bar_chart(top_10_bat, color="#673AB7", height=220) # Deep ICC Purple
        
        st.subheader("🎯 Top 10 Wicket Takers")
        top_10_bowl = bowler_wickets.head(10)
        st.bar_chart(top_10_bowl, color="#E91E63", height=220) # Pink/Magenta

    # ==========================================
    # FULL WIDTH: EVERY SINGLE MATCH STATS
    # ==========================================
    st.markdown("---")
    st.subheader("📜 Tournament Match History")
    
    match_results = match_level_df[['date', 'batting_team', 'bowling_team', 'match_won_by', 'player_of_match', 'venue']].copy()
    match_results.columns = ['Date', 'Team 1', 'Team 2', 'Winner', 'Player of the Match', 'Venue']
    
    match_results['Date'] = pd.to_datetime(match_results['Date'], errors='coerce')
    match_results = match_results.sort_values(by='Date', ascending=False)
    match_results['Date'] = match_results['Date'].dt.strftime('%Y-%m-%d').fillna('Unknown')
    
    st.dataframe(match_results, use_container_width=True, hide_index=True)