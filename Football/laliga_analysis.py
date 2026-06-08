import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/laliga_combined.csv", low_memory=False)
    except FileNotFoundError:
        df = pd.read_csv("../data/laliga_combined.csv", low_memory=False)
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    return df

def generate_league_table(df):
    if df.empty:
        return pd.DataFrame(columns=['Team', 'Played', 'Won', 'Drawn', 'Lost', 'Goals For', 'Goals Against', 'Goal Difference', 'Points'])

    teams = pd.concat([df['home_team'], df['away_team']]).dropna().unique()
    table = []
    
    for team in teams:
        home_games = df[df['home_team'] == team]
        away_games = df[df['away_team'] == team]
        
        played = len(home_games) + len(away_games)
        if played == 0: continue
            
        wins = len(home_games[home_games['ftr'] == 'H']) + len(away_games[away_games['ftr'] == 'A'])
        draws = len(home_games[home_games['ftr'] == 'D']) + len(away_games[away_games['ftr'] == 'D'])
        losses = played - wins - draws
        
        gf = int(home_games['fthg'].sum() + away_games['ftag'].sum())
        ga = int(home_games['ftag'].sum() + away_games['fthg'].sum())
        gd = gf - ga
        points = (wins * 3) + (draws * 1)
        
        table.append({
            'Team': team, 'Played': played, 'Won': wins, 'Drawn': draws, 'Lost': losses, 
            'Goals For': gf, 'Goals Against': ga, 'Goal Difference': gd, 'Points': points
        })
        
    if not table:
        return pd.DataFrame(columns=['Team', 'Played', 'Won', 'Drawn', 'Lost', 'Goals For', 'Goals Against', 'Goal Difference', 'Points'])

    res_df = pd.DataFrame(table).sort_values(by=['Points', 'Goal Difference', 'Goals For'], ascending=[False, False, False])
    res_df.index = range(1, len(res_df) + 1)
    return res_df

def run_laliga_analysis():
    st.header("La Liga Analytics Hub")
    st.markdown("---")
    
    with st.spinner("Loading La Liga history..."):
        df = load_data()
        
    st.write("🗓️ **Select La Liga Season:**")
    seasons = sorted(df['season'].dropna().unique().tolist(), reverse=True)
    selected_season = st.selectbox("Season Dropdown", seasons, label_visibility="collapsed")
    
    filtered_df = df[df['season'] == selected_season]
    
    # Restored Tabs
    tab1, tab2 = st.tabs(["🏆 League Standings & Stats", "🔍 Match Inspector"])
    
    # ==========================================
    # TAB 1: LEAGUE TABLE AND GRAPHICS
    # ==========================================
    with tab1:
        league_table = generate_league_table(filtered_df)
        
        total_goals = int(filtered_df['fthg'].sum() + filtered_df['ftag'].sum())
        home_wins = len(filtered_df[filtered_df['ftr'] == 'H'])
        away_wins = len(filtered_df[filtered_df['ftr'] == 'A'])
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Matches Played", len(filtered_df))
        c2.metric("Total Goals", total_goals)
        c3.metric("Home Win %", f"{round((home_wins/len(filtered_df))*100, 1)}%" if len(filtered_df)>0 else "0%")
        c4.metric("Away Win %", f"{round((away_wins/len(filtered_df))*100, 1)}%" if len(filtered_df)>0 else "0%")
        
        st.markdown("---")
        
        col_table, col_charts = st.columns([1.2, 1])
        
        with col_table:
            st.subheader(f"Points Table: {selected_season}")
            st.dataframe(league_table, use_container_width=True, height=600)
            
        with col_charts:
            if not league_table.empty:
                league_table['Goals For'] = pd.to_numeric(league_table['Goals For'])
                league_table['Goals Against'] = pd.to_numeric(league_table['Goals Against'])
                
                st.subheader("⚔️ Attacking Power (Goals Scored)")
                top_attack = league_table.sort_values(by='Goals For', ascending=True).tail(10)
                fig1 = px.bar(top_attack, x='Goals For', y='Team', orientation='h', color_discrete_sequence=['#EA0437'])
                fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig1, use_container_width=True)
                
                st.subheader("🛡️ Defensive Walls (Fewest Goals Conceded)")
                top_defense = league_table.sort_values(by='Goals Against', ascending=False).tail(10)
                fig2 = px.bar(top_defense, x='Goals Against', y='Team', orientation='h', color_discrete_sequence=['#FFC300'])
                fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("No data available to generate charts for this season.")

    # ==========================================
    # TAB 2: LA LIGA MATCH INSPECTOR
    # ==========================================
    with tab2:
        st.subheader("🔍 Select a Match to Inspect")
        
        if filtered_df.empty:
            st.info("No match data available for this season.")
        else:
            date_strings = filtered_df['date'].dt.strftime('%Y-%m-%d').fillna('Unknown Date')
            filtered_df['display_name'] = date_strings + " | " + filtered_df['home_team'].astype(str) + " vs " + filtered_df['away_team'].astype(str)
            
            selected_match_str = st.selectbox("Choose Match", filtered_df['display_name'].tolist(), label_visibility="collapsed")
            
            if selected_match_str:
                match_subset = filtered_df[filtered_df['display_name'] == selected_match_str]
                
                if not match_subset.empty:
                    m = match_subset.iloc[0]
                    date_display = m['date'].strftime('%d %B %Y') if pd.notnull(m['date']) else 'Unknown Date'
                    
                    st.markdown(f"""
                    <div style='background-color: #1A1A1A; padding: 30px; border-radius: 10px; margin-top: 20px; border-left: 6px solid #EA0437;'>
                        <p style='text-align: center; color: #FFC300; font-size: 14px; margin: 0; padding-bottom: 10px; font-weight: bold; letter-spacing: 2px;'>FULL TIME RESULT • {date_display.upper()}</p>
                        <h2 style='text-align: center; color: white; margin: 0; font-size: 38px;'>
                            {m['home_team']} <span style='color: #EA0437; padding: 0 20px;'>{int(m['fthg'])} - {int(m['ftag'])}</span> {m['away_team']}
                        </h2>
                        <p style='text-align: center; color: gray; font-size: 12px; margin: 0; padding-top: 20px;'>Match data limited to final scorelines for this historical dataset.</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.warning("Match details could not be loaded.")