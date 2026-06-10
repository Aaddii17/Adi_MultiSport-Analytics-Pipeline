import streamlit as st
import pandas as pd
import plotly.express as px
import os

@st.cache_data
def load_copa_data():
    data_dir = "data/" if os.path.exists("data/") else "../data/"
    try:
        df_summary = pd.read_csv(os.path.join(data_dir, "copa_summary_clean.csv"))
    except FileNotFoundError:
        df_summary = pd.DataFrame()
        
    try:
        df_matches = pd.read_csv(os.path.join(data_dir, "copa_matches_clean.csv"))
    except FileNotFoundError:
        df_matches = pd.DataFrame()
        
    return df_summary, df_matches

def run_copa_analysis():
    st.header("🌎 CONMEBOL Copa America Hub")
    st.markdown("---")
    
    with st.spinner("Loading South American History..."):
        df_summary, df_matches = load_copa_data()
        
    has_goal_data = not df_summary.empty and 'Average Goals' in df_summary.columns
    
    tab_names = ["👑 Kings of the Continent"]
    if has_goal_data:
        tab_names.append("⚽ Goals & Entertainment")
    tab_names.append("🔍 Match Inspector (2001-2021)")
    
    tabs = st.tabs(tab_names)
    
    # ==========================================
    # TAB 1: TOURNAMENT HISTORY & MOST WINS
    # ==========================================
    with tabs[0]:
        st.subheader("🌟 Most Copa America Titles")
        if not df_summary.empty:
            champions = df_summary['Champion'].value_counts().reset_index()
            champions.columns = ['Nation', 'Trophies Won']
            
            fig_champs = px.bar(champions, x='Nation', y='Trophies Won', 
                                color_discrete_sequence=['#D4AF37'],
                                text='Trophies Won')
            fig_champs.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", showlegend=False)
            st.plotly_chart(fig_champs, use_container_width=True)
            
            st.markdown("---")
            st.subheader("Tournament History")
            display_cols = ['Year', 'Host', 'Champion', 'Runner-Up', 'Teams', 'Matches']
            available_cols = [c for c in display_cols if c in df_summary.columns]
            st.dataframe(df_summary[available_cols].sort_values(by='Year', ascending=False), use_container_width=True)
        else:
            st.warning("Tournament data not found.")

    # ==========================================
    # TAB 2 (OPTIONAL): GOALS & ENTERTAINMENT
    # ==========================================
    current_tab_idx = 1
    
    if has_goal_data:
        with tabs[current_tab_idx]:
            st.subheader("📈 The Evolution of South American Football")
            st.markdown("Tracking the average goals per game to visualize the shift between defensive and attacking eras.")
            
            plot_df = df_summary.copy()
            plot_df['Year'] = pd.to_numeric(plot_df['Year'].astype(str).str[:4], errors='coerce')
            plot_df = plot_df.dropna(subset=['Year']).sort_values(by='Year')
            
            fig_goals = px.line(plot_df, x='Year', y='Average Goals', markers=True,
                                color_discrete_sequence=['#00B4D8'])
            
            average_all_time = plot_df['Average Goals'].mean()
            fig_goals.add_hline(y=average_all_time, line_dash="dot", line_color="gray", annotation_text="All-Time Average")
            
            fig_goals.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_goals, use_container_width=True)
            
        current_tab_idx += 1

    # ==========================================
    # TAB 3 (or 2): DYNAMIC MATCH INSPECTOR
    # ==========================================
    with tabs[current_tab_idx]:
        st.subheader("🔍 Modern Match Analysis")
        if not df_matches.empty:
            
            # FIX: Drop any corrupted rows or empty entries where scores are missing or NaN
            df_matches = df_matches.dropna(subset=['Home Score', 'Away Score', 'Home Team', 'Away Team'])
            
            years = sorted(df_matches['Year'].dropna().unique().tolist(), reverse=True)
            col1, col2 = st.columns([1, 3])
            with col1:
                selected_year = st.selectbox("Select Year", years)
                
            filtered_matches = df_matches[df_matches['Year'] == selected_year].copy()
            
            # Build clean display names from fully verified data rows
            filtered_matches['display_name'] = (
                filtered_matches['Round'].astype(str) + " | " + 
                filtered_matches['Home Team'].astype(str) + " vs " + 
                filtered_matches['Away Team'].astype(str)
            )
            
            match_options = filtered_matches['display_name'].tolist()
            
            if not match_options:
                st.info("No valid completed matches found for this year.")
            else:
                selected_match_str = st.selectbox("Select Match", match_options)
                
                if selected_match_str:
                    m = filtered_matches[filtered_matches['display_name'] == selected_match_str].iloc[0]
                    
                    # Scoreboard safely casts clean, checked numerical values to integers
                    st.markdown(f"""
                    <div style='background-color: #0B1D3A; padding: 30px; border-radius: 10px; margin-top: 15px; border-left: 5px solid #D4AF37;'>
                        <p style='text-align: center; color: #D4AF37; font-size: 14px; margin: 0; padding-bottom: 10px; font-weight: bold; letter-spacing: 2px;'>{str(m['Round']).upper()} • {m['Date']}</p>
                        <h2 style='text-align: center; color: white; margin: 0; font-size: 45px;'>
                            {m['Home Team']} <span style='color: #00B4D8; padding: 0 20px;'>{int(m['Home Score'])} - {int(m['Away Score'])}</span> {m['Away Team']}
                        </h2>
                    </div>
                    """, unsafe_allow_html=True)
                
        else:
            st.warning("Match data not found.")