import streamlit as st
import ipl_analysis
import sa20_analysis
import cpl_analysis

st.set_page_config(page_title="Multi-Sport Analytics", layout="wide")
st.title("🏏 Real-Time Multi-Sport Analytics & Prediction Pipeline")

st.sidebar.title("Navigation")
sport_selected = st.sidebar.radio("Select Sport", ["Cricket", "Football"])

if sport_selected == "Cricket":
    st.sidebar.subheader("Cricket Category")
    category = st.sidebar.selectbox("Select Category", ["Men's Leagues", "Men's International", "Women's Leagues", "Women's International"])
    
    if category == "Men's Leagues":
        tournament = st.sidebar.selectbox("Select Tournament", ["IPL", "SA20", "Caribbean Premier League", "Big Bash League"])
        
        if tournament == "IPL":
            ipl_analysis.run_ipl_analysis() 
        elif tournament == "SA20":
            sa20_analysis.run_sa20_analysis()
        elif tournament == "Caribbean Premier League":
            cpl_analysis.run_cpl_analysis()
        else:
            st.info(f"🚧 {tournament} is next in the pipeline. Finish CPL first!")
            
elif sport_selected == "Football":
    st.info("🚧 Football section will be started only after Cricket is 100% complete.")