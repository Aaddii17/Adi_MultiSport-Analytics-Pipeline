import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("data/bundesliga_combined.csv", low_memory=False)
    except FileNotFoundError:
        df = pd.read_csv("../data/bundesliga_combined.csv", low_memory=False)
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

def run_bundesliga_analysis():
    st.header("🇩🇪 Bundesliga Analytics Hub")
    st.markdown("---")
    
    with st.spinner("Loading Bundesliga history..."):
        df = load_data()
        
    st.write("🗓️ **Select Bundesliga Season:**")
    seasons = sorted(df['season'].dropna().unique().tolist(), reverse=True)
    selected_season = st.selectbox("Season Dropdown", seasons, label_visibility="collapsed")
    
    filtered_df = df[df['season'] == selected_season]
    
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
                # Bundesliga Red
                fig1 = px.bar(top_attack, x='Goals For', y='Team', orientation='h', color_discrete_sequence=['#D71920'])
                fig1.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig1, use_container_width=True)
                
                st.subheader("🛡️ Defensive Walls (Fewest Goals Conceded)")
                top_defense = league_table.sort_values(by='Goals Against', ascending=False).tail(10)
                # Deep Gray/Black
                fig2 = px.bar(top_defense, x='Goals Against', y='Team', orientation='h', color_discrete_sequence=['#4A4A4A'])
                fig2.update_layout(margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig2, use_container_width=True)
            else:
                st.warning("No data available to generate charts for this season.")

    # ==========================================
    # TAB 2: DYNAMIC MATCH INSPECTOR
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
                    
                    advanced_stats_exist = (m.get('hs', 0) + m.get('as', 0) + m.get('hc', 0) + m.get('ac', 0)) > 0
                    
                    if advanced_stats_exist:
                        st.markdown(f"""
                        <div style='background-color: #D71920; padding: 15px; border-radius: 10px; margin-bottom: 15px;'>
                            <h2 style='text-align: center; color: white; margin: 0; font-size: 28px;'>{m['home_team']} <span style='color: #1A1A1A;'>{int(m['fthg'])} - {int(m['ftag'])}</span> {m['away_team']}</h2>
                            <p style='text-align: center; color: #FFFFFF; font-size: 14px; margin: 0; padding-top: 5px; font-weight: bold;'>HALF-TIME: {int(m['hthg'])} - {int(m['htag'])}</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        def stat_row(home_stat, stat_name, away_stat):
                            st.markdown(f"""
                            <table style="width: 100%; background-color: transparent; border-bottom: 1px solid #333; margin-bottom: 0px;">
                                <tr>
                                    <td style="width: 33%; text-align: left; color: white; font-size: 22px; font-weight: bold; padding: 8px 0; border: none;">{int(home_stat)}</td>
                                    <td style="width: 34%; text-align: center; color: #D71920; font-size: 14px; font-weight: bold; white-space: nowrap; padding: 8px 0; border: none; letter-spacing: 1px;">{stat_name.upper()}</td>
                                    <td style="width: 33%; text-align: right; color: white; font-size: 22px; font-weight: bold; padding: 8px 0; border: none;">{int(away_stat)}</td>
                                </tr>
                            </table>
                            """, unsafe_allow_html=True)

                        st.markdown("<h4 style='text-align: center; margin-top: 10px; margin-bottom: 5px;'>MATCH STATS</h4>", unsafe_allow_html=True)
                        st.markdown("<hr style='border: 1.5px solid #D71920; margin-top: 0; margin-bottom: 10px;'>", unsafe_allow_html=True)

                        stat_row(m.get('hst', 0), "Shots on Target", m.get('ast', 0))
                        stat_row(m.get('hs', 0), "Total Shots", m.get('as', 0))
                        stat_row(m.get('hc', 0), "Corners", m.get('ac', 0))
                        stat_row(m.get('hf', 0), "Fouls Conceded", m.get('af', 0))
                        stat_row(m.get('hy', 0), "Yellow Cards", m.get('ay', 0))
                        stat_row(m.get('hr', 0), "Red Cards", m.get('ar', 0))
                        
                    else:
                        st.markdown(f"""
                        <div style='background-color: #1A1A1A; padding: 30px; border-radius: 10px; margin-top: 20px; border-left: 6px solid #D71920;'>
                            <p style='text-align: center; color: gray; font-size: 14px; margin: 0; padding-bottom: 10px; font-weight: bold; letter-spacing: 2px;'>FULL TIME RESULT • {date_display.upper()}</p>
                            <h2 style='text-align: center; color: white; margin: 0; font-size: 38px;'>
                                {m['home_team']} <span style='color: #D71920; padding: 0 20px;'>{int(m['fthg'])} - {int(m['ftag'])}</span> {m['away_team']}
                            </h2>
                            <p style='text-align: center; color: gray; font-size: 12px; margin: 0; padding-top: 20px;'>Historical dataset: Advanced performance metrics are unavailable for this match.</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Match details could not be loaded.")