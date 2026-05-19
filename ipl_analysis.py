import streamlit as st
import pandas as pd

# Cache the data so it loads instantly after the first time
@st.cache_data
def load_data():
    df = pd.read_csv("data/ipl_ball_by_ball_2008_2025.csv", low_memory=False)
    return df

def run_ipl_analysis():
    st.header("🏏 IPL Analytics Hub")
    st.markdown("---")
    
    # Load the data
    with st.spinner("Crunching millions of data points..."):
        df = load_data()
    
    # ==========================================
    # FILTERS & DATA PREP
    # ==========================================
    st.write("🗓️ **Select IPL Season:**")
    seasons = sorted(df['season'].dropna().unique().tolist(), reverse=True)
    seasons.insert(0, "All-Time") 
    
    selected_season = st.selectbox("Season Dropdown", seasons, label_visibility="collapsed")
    
    if selected_season != "All-Time":
        filtered_df = df[df['season'] == selected_season]
    else:
        filtered_df = df
        
    match_level_df = filtered_df.drop_duplicates(subset=['match_id'])
    
    # ==========================================
    # TOP LEVEL METRICS
    # ==========================================
    total_matches = match_level_df['match_id'].nunique()
    
    # Orange Cap
    batsman_runs = filtered_df.groupby('batter')['runs_batter'].sum().sort_values(ascending=False)
    orange_cap = batsman_runs.index[0] if not batsman_runs.empty else "-"
    orange_cap_runs = int(batsman_runs.iloc[0]) if not batsman_runs.empty else 0
    
    # Purple Cap
    valid_wickets = ['bowled', 'caught', 'lbw', 'stumped', 'caught and bowled', 'hit wicket']
    bowler_wickets = filtered_df[filtered_df['wicket_kind'].isin(valid_wickets)].groupby('bowler')['player_out'].count().sort_values(ascending=False)
    purple_cap = bowler_wickets.index[0] if not bowler_wickets.empty else "-"
    purple_cap_wickets = int(bowler_wickets.iloc[0]) if not bowler_wickets.empty else 0
    
    # MVP
    mvp_counts = match_level_df['player_of_match'].value_counts()
    top_mvp = mvp_counts.index[0] if not mvp_counts.empty else "-"
    top_mvp_awards = int(mvp_counts.iloc[0]) if not mvp_counts.empty else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Matches Played", total_matches)
    col2.metric("🟠 Orange Cap", f"{orange_cap}", f"↑ {orange_cap_runs} Runs")
    col3.metric("🟣 Purple Cap", f"{purple_cap}", f"↑ {purple_cap_wickets} Wickets")
    col4.metric("⭐ Most MVP", f"{top_mvp}", f"↑ {top_mvp_awards} Awards")
    
    st.markdown("---")

    # ==========================================
    # SPLIT LAYOUT: POINTS TABLE & STACKED CHARTS (MOVED UP)
    # ==========================================
    col_table, col_charts = st.columns([1.5, 1]) 
    
    with col_table:
        st.subheader("📊 Points Table")
        
        # --- Dynamic Points Table Calculation ---
        # Get a list of all unique teams that played in the selected season
        all_teams = pd.concat([match_level_df['batting_team'], match_level_df['bowling_team']]).dropna().unique()
        
        points_data = []
        for team in all_teams:
            # Matches Played (where they were either batting or bowling team)
            played = len(match_level_df[(match_level_df['batting_team'] == team) | (match_level_df['bowling_team'] == team)])
            # Matches Won
            wins = len(match_level_df[match_level_df['match_won_by'] == team])
            # Matches Lost (They played, there was a winner, and the winner wasn't them)
            losses = len(match_level_df[((match_level_df['batting_team'] == team) | (match_level_df['bowling_team'] == team)) & 
                                        (match_level_df['match_won_by'].notna()) & 
                                        (match_level_df['match_won_by'] != team)])
            # Ties / No Results
            nr_tie = played - wins - losses
            # Points (2 for win, 1 for tie/NR)
            pts = (wins * 2) + (nr_tie * 1)
            
            points_data.append({'Team': team, 'M': played, 'W': wins, 'L': losses, 'NR/Tie': nr_tie, 'Pts': pts})
            
        # Convert to DataFrame and sort by Points (highest first), then Wins
        points_df = pd.DataFrame(points_data).sort_values(by=['Pts', 'W'], ascending=[False, False])
        # Add index starting from 1 for rankings
        points_df.index = range(1, len(points_df) + 1)
        
        # Display the table
        st.dataframe(points_df, use_container_width=True, height=520)
        
    with col_charts:
        st.subheader("🟠 Top 10 Run Scorers")
        top_10_bat = batsman_runs.head(10)
        st.bar_chart(top_10_bat, color="#ff9933", height=220) 
        
        st.subheader("🟣 Top 10 Wicket Takers")
        top_10_bowl = bowler_wickets.head(10)
        st.bar_chart(top_10_bowl, color="#9933ff", height=220)

    # ==========================================
    # FULL WIDTH: EVERY SINGLE MATCH STATS (MOVED DOWN)
    # ==========================================
    st.markdown("---")
    st.subheader("📜 Every Single Match Stats")
    
    match_results = match_level_df[['date', 'batting_team', 'bowling_team', 'match_won_by', 'player_of_match', 'venue', 'toss_winner', 'toss_decision']].copy()
    match_results.columns = ['Date', 'Team 1', 'Team 2', 'Winner', 'Player of the Match', 'Venue', 'Toss Winner', 'Toss Decision']
    match_results = match_results.sort_values(by='Date', ascending=False)
    
    st.dataframe(match_results, use_container_width=True, hide_index=True)