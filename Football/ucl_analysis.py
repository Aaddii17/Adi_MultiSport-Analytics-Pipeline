import streamlit as st
import pandas as pd
import plotly.express as px
import os

@st.cache_data
def load_ucl_data():
    data_dir = "data/" if os.path.exists("data/") else "../data/"
    
    try:
        df_finals = pd.read_csv(os.path.join(data_dir, "ucl_finals_clean.csv"))
    except FileNotFoundError:
        df_finals = pd.DataFrame()
        
    try:
        df_alltime = pd.read_csv(os.path.join(data_dir, "ucl_alltime_clean.csv"))
    except FileNotFoundError:
        df_alltime = pd.DataFrame()
        
    try:
        df_goals = pd.read_csv(os.path.join(data_dir, "ucl_goals_clean.csv"))
    except FileNotFoundError:
        df_goals = pd.DataFrame()
        
    return df_finals, df_alltime, df_goals

def run_ucl_analysis():
    st.header("⭐ UEFA Champions League Analytics Hub")
    st.markdown("---")
    
    with st.spinner("Loading European History..."):
        df_finals, df_alltime, df_goals = load_ucl_data()
        
    tab1, tab2, tab3 = st.tabs(["👑 All-Time Hall of Fame", "🏟️ Finals History", "⚽ Goal Event Analysis (2016-2022)"])
    
    # ==========================================
    # TAB 1: ALL-TIME HALL OF FAME
    # ==========================================
    with tab1:
        st.subheader("The Kings of Europe")
        if not df_alltime.empty:
            st.markdown("This table ranks every club's historical performance in the European Cup / Champions League.")
            
            # Recalculate true points (3 for a Win, 1 for a Draw)
            if 'W' in df_alltime.columns and 'D' in df_alltime.columns:
                df_alltime['W'] = pd.to_numeric(df_alltime['W'], errors='coerce').fillna(0)
                df_alltime['D'] = pd.to_numeric(df_alltime['D'], errors='coerce').fillna(0)
                df_alltime['Pt.'] = (df_alltime['W'] * 3) + (df_alltime['D'] * 1)
            
            # Expand abbreviations into Full Forms
            rename_dict = {
                '#': 'Rank',
                'M.': 'Matches Played',
                'W': 'Wins',
                'D': 'Draws',
                'L': 'Losses',
                'Dif': 'Goal Difference',
                'Pt.': 'Points'
            }
            df_alltime.rename(columns={k: v for k, v in rename_dict.items() if k in df_alltime.columns}, inplace=True)
                
            st.dataframe(df_alltime, use_container_width=True, height=600)
        else:
            st.warning("All-Time data not found. Please run the ETL pipeline.")

    # ==========================================
    # TAB 2: FINALS HISTORY TRACKER
    # ==========================================
    with tab2:
        st.subheader("Champions League Finals (1955 - 2023)")
        if not df_finals.empty:
            
            # Find the corrupted Attendance column dynamically and rename it
            attend_col = [col for col in df_finals.columns if 'Attend' in col]
            if attend_col:
                df_finals.rename(columns={attend_col[0]: 'Attendance'}, inplace=True)
            
            desired_cols = ['Season', 'Winners', 'Score', 'Runners-up', 'Venue', 'Attendance']
            available_cols = [col for col in desired_cols if col in df_finals.columns]
            
            display_finals = df_finals[available_cols].copy()
            
            # REGEX FIX: Swap the corrupted non-ASCII "boxes" in Season and Score with clean hyphens
            if 'Season' in display_finals.columns:
                display_finals['Season'] = display_finals['Season'].astype(str).str.replace(r'[^\x00-\x7F]+', '-', regex=True)
            if 'Score' in display_finals.columns:
                display_finals['Score'] = display_finals['Score'].astype(str).str.replace(r'[^\x00-\x7F]+', '-', regex=True)

            st.dataframe(display_finals, use_container_width=True, height=600)
        else:
            st.warning("Finals data not found. Please run the ETL pipeline.")

    # ==========================================
    # TAB 3: GOAL EVENT ANALYSIS
    # ==========================================
    with tab3:
        st.subheader("How the Best Score Goals")
        if not df_goals.empty and 'GOAL_DESC' in df_goals.columns:
            st.markdown("Analysis of all goal events recorded between the 2016 and 2022 Champions League campaigns.")
            
            col1, col2 = st.columns(2)
            
            with col1:
                goal_types = df_goals['GOAL_DESC'].value_counts().reset_index()
                goal_types.columns = ['Goal Type', 'Count']
                
                fig = px.pie(goal_types, values='Count', names='Goal Type', hole=0.4, 
                             color_discrete_sequence=['#00143F', '#0055A4', '#00A6EB', '#C0C0C0', '#FFFFFF'])
                fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                st.plotly_chart(fig, use_container_width=True)
                
            with col2:
                if 'DURATION' in df_goals.columns:
                    st.markdown("**When are goals scored?**")
                    df_goals['Minute'] = pd.to_numeric(df_goals['DURATION'], errors='coerce')
                    
                    fig2 = px.histogram(df_goals, x='Minute', nbins=10, 
                                        color_discrete_sequence=['#00A6EB'])
                    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                       xaxis_title="Minute of Match", yaxis_title="Goals Scored")
                    st.plotly_chart(fig2, use_container_width=True)
        else:
            st.warning("Goal event data not found. Please run the ETL pipeline.")