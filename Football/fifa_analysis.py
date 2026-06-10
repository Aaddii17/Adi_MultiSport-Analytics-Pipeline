import streamlit as st
import pandas as pd
import plotly.express as px
import os
import math

@st.cache_data
def load_fifa_data():
    data_dir = "data/" if os.path.exists("data/") else "../data/"
    try:
        df_wc = pd.read_csv(os.path.join(data_dir, "fifa_worldcup_clean.csv"))
    except FileNotFoundError:
        df_wc = pd.DataFrame()
        
    try:
        df_matches = pd.read_csv(os.path.join(data_dir, "fifa_matches_clean.csv"))
    except FileNotFoundError:
        df_matches = pd.DataFrame()
        
    return df_wc, df_matches

def generate_alltime_table(df):
    if df.empty: return pd.DataFrame()

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
        
        gf = int(home_games['home_score'].sum() + away_games['away_score'].sum())
        ga = int(home_games['away_score'].sum() + away_games['home_score'].sum())
        gd = gf - ga
        points = (wins * 3) + (draws * 1)
        
        table.append({
            'Nation': team, 'Matches': played, 'Wins': wins, 'Draws': draws, 'Losses': losses, 
            'GF': gf, 'GA': ga, 'GD': gd, 'Points': points
        })
        
    res_df = pd.DataFrame(table).sort_values(by=['Points', 'GD', 'GF'], ascending=[False, False, False])
    res_df.index = range(1, len(res_df) + 1)
    return res_df

# Helper function to clean up encoding artifacts in names on the fly
def clean_name(name):
    if pd.isna(name): return "Unknown"
    return str(name).replace('Â', '').replace('Ä‡', 'ć').strip()

def run_fifa_analysis():
    st.header("🏆 FIFA World Cup Analytics Hub")
    st.markdown("---")
    
    with st.spinner("Loading World Cup History..."):
        df_wc, df_matches = load_fifa_data()
        
    tab1, tab2, tab3, tab4 = st.tabs(["📜 Tournament History", "🥾 Golden Boot", "🌍 All-Time Leaderboard", "🔍 Match Inspector"])
    
    # ==========================================
    # TAB 1: TOURNAMENT HISTORY & MOST WINS
    # ==========================================
    with tab1:
        st.subheader("🌟 Most World Cup Titles (All-Time)")
        if not df_wc.empty:
            # Aggregate the winners
            champions = df_wc['Champion'].value_counts().reset_index()
            champions.columns = ['Nation', 'Trophies Won']
            
            # Display as a clean bar chart
            fig_champs = px.bar(champions, x='Nation', y='Trophies Won', 
                                color='Trophies Won', color_continuous_scale='YlOrBr',
                                text='Trophies Won')
            fig_champs.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
            st.plotly_chart(fig_champs, use_container_width=True)
            
            st.markdown("---")
            st.subheader("World Cup Finals History")
            display_wc = df_wc[['Year', 'Host', 'Champion', 'Runner-Up', 'Teams', 'Matches', 'Attendance']].copy()
            st.dataframe(display_wc.sort_values(by='Year', ascending=False), use_container_width=True)
        else:
            st.warning("Tournament data not found.")

    # ==========================================
    # TAB 2: GOLDEN BOOT
    # ==========================================
    with tab2:
        st.subheader("Top Goalscorers by Tournament")
        if not df_wc.empty and 'Top Scorer Goals' in df_wc.columns:
            fig_gb = px.bar(df_wc.sort_values(by='Year', ascending=False), 
                            x='Top Scorer Goals', y='Year', orientation='h',
                            text='Top Scorer Name',
                            color='Top Scorer Goals', color_continuous_scale='YlOrBr')
            fig_gb.update_layout(height=700, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_gb, use_container_width=True)
        else:
            st.warning("Golden boot data not extracted.")

    # ==========================================
    # TAB 3: ALL-TIME LEADERBOARD
    # ==========================================
    with tab3:
        st.subheader("Global Power Rankings (1930 - 2022)")
        st.markdown("Ranked by total points accumulated in World Cup history (3 for a Win, 1 for a Draw).")
        if not df_matches.empty:
            all_time_table = generate_alltime_table(df_matches)
            st.dataframe(all_time_table, use_container_width=True, height=600)
        else:
            st.warning("Match data not found.")

    # ==========================================
    # TAB 4: DYNAMIC MATCH INSPECTOR (SIMPLIFIED)
    # ==========================================
    with tab4:
        st.subheader("🔍 Deep Match Analysis")
        if not df_matches.empty:
            years = sorted(df_matches['Year'].dropna().unique().tolist(), reverse=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                selected_year = st.selectbox("Select Year", years)
                
            filtered_matches = df_matches[df_matches['Year'] == selected_year].copy()
            filtered_matches['display_name'] = filtered_matches['Round'] + " | " + filtered_matches['home_team'] + " vs " + filtered_matches['away_team']
            
            with col2:
                selected_match_str = st.selectbox("Select Match", filtered_matches['display_name'].tolist())
                
            if selected_match_str:
                m = filtered_matches[filtered_matches['display_name'] == selected_match_str].iloc[0]
                
                # Robust Penalty Shootout Check (Ensures 3-3 Final triggers the 4-2 penalty text)
                penalties = ""
                home_pen = m.get('home_pen')
                away_pen = m.get('away_pen')
                if pd.notna(home_pen) and pd.notna(away_pen):
                    try:
                        if float(home_pen) >= 0 and float(away_pen) >= 0:
                            penalties = f"<br><span style='font-size: 20px; color: #E0E0E0;'>*(Won on Penalties: {int(float(home_pen))} - {int(float(away_pen))})*</span>"
                    except ValueError:
                        pass
                    
                st.markdown(f"""
                <div style='background-color: #004B23; padding: 25px; border-radius: 10px; margin-top: 15px; border: 2px solid #D4AF37;'>
                    <p style='text-align: center; color: #D4AF37; font-size: 16px; margin: 0; padding-bottom: 10px; font-weight: bold; letter-spacing: 2px;'>{str(m['Round']).upper()} • {m['Date']}</p>
                    <h2 style='text-align: center; color: white; margin: 0; font-size: 42px;'>
                        {m['home_team']} <span style='color: #D4AF37; padding: 0 15px;'>{int(m['home_score'])} - {int(m['away_score'])}</span> {m['away_team']}
                    </h2>
                    <p style='text-align: center; margin: 0;'>{penalties}</p>
                </div>
                """, unsafe_allow_html=True)
                
                # Match Info Row
                st.markdown("<br>", unsafe_allow_html=True)
                c1, c2, c3 = st.columns(3)
                c1.metric("🏟️ Venue", str(m.get('Venue', 'Unknown')))
                c2.metric("👥 Attendance", f"{m.get('Attendance', 0):,.0f}" if pd.notna(m.get('Attendance')) else "Unknown")
                c3.metric("⚖️ Referee", clean_name(m.get('Referee')))
                
                st.markdown("<hr style='border: 1px solid #333;'>", unsafe_allow_html=True)
                
                # Simplified Head-to-Head Stats
                if pd.notna(m.get('home_xg')) and pd.notna(m.get('away_xg')):
                    st.markdown("<h4 style='text-align: center; color: #D4AF37; margin-bottom: 20px;'>HEAD-TO-HEAD STATS</h4>", unsafe_allow_html=True)
                    
                    def stat_row(home_stat, stat_name, away_stat, description=""):
                        st.markdown(f"""
                        <table style="width: 100%; background-color: transparent; border-bottom: 1px solid #222; margin-bottom: 5px;">
                            <tr>
                                <td style="width: 33%; text-align: left; color: white; font-size: 22px; font-weight: bold; padding: 12px 0; border: none;">{home_stat}</td>
                                <td style="width: 34%; text-align: center; border: none; padding: 12px 0;">
                                    <div style="color: gray; font-size: 15px; font-weight: bold; letter-spacing: 1px;">{stat_name.upper()}</div>
                                    <div style="color: #666; font-size: 11px;">{description}</div>
                                </td>
                                <td style="width: 33%; text-align: right; color: white; font-size: 22px; font-weight: bold; padding: 12px 0; border: none;">{away_stat}</td>
                            </tr>
                        </table>
                        """, unsafe_allow_html=True)
                        
                    stat_row(m['home_xg'], "Expected Goals (xG)", m['away_xg'], "How many goals a team *should* have scored based on shot quality.")
                    
                    if pd.notna(m.get('home_manager')) and pd.notna(m.get('away_manager')):
                        stat_row(clean_name(m['home_manager']), "Team Manager", clean_name(m['away_manager']))