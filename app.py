import streamlit as st

# --- IMPORT CRICKET MODULES ---
from Cricket import ipl_analysis
from Cricket import sa20_analysis
from Cricket import cpl_analysis
from Cricket import bbl_analysis
from Cricket import odi_analysis
from Cricket import odiwc_analysis
from Cricket import t20i_analysis
from Cricket import t20wc_analysis
from Cricket import wpl_analysis
from Cricket import wbbl_analysis
from Cricket import wt20i_analysis
from Cricket import wodi_analysis
from Cricket import wtest_analysis
from Cricket import wt20wc_analysis
from Cricket import wodiwc_analysis

# --- IMPORT FOOTBALL MODULES ---
from Football import epl_analysis
from Football import laliga_analysis
from Football import seriea_analysis
from Football import bundesliga_analysis
from Football import ligue1_analysis
from Football import mls_analysis

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Multi-Sport Analytics",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title("Navigation")
    
    sport = st.sidebar.radio("Select Sport", ["Cricket", "Football"])
    
    st.sidebar.markdown("---")

    if sport == "Cricket":
        category = st.sidebar.selectbox(
            "Cricket Category", 
            ["Men's Leagues", "Men's International", "Women's Leagues", "Women's International"]
        )
        
        # ==========================================
        # 1. MEN'S LEAGUES
        # ==========================================
        if category == "Men's Leagues":
            tournament = st.sidebar.selectbox(
                "Select Tournament", 
                ["IPL", "SA20", "Caribbean Premier League", "Big Bash League"]
            )
            
            if tournament == "IPL": ipl_analysis.run_ipl_analysis()
            elif tournament == "SA20": sa20_analysis.run_sa20_analysis()
            elif tournament == "Caribbean Premier League": cpl_analysis.run_cpl_analysis()
            elif tournament == "Big Bash League": bbl_analysis.run_bbl_analysis()

        # ==========================================
        # 2. MEN'S INTERNATIONAL
        # ==========================================
        elif category == "Men's International":
            format_type = st.sidebar.selectbox(
                "Select Format", 
                ["One Day Internationals", "ODI World Cup", "T20 Internationals", "T20 World Cup"]
            )
            
            if format_type == "One Day Internationals": odi_analysis.run_odi_analysis()
            elif format_type == "ODI World Cup": odiwc_analysis.run_odiwc_analysis()
            elif format_type == "T20 Internationals": t20i_analysis.run_t20i_analysis()
            elif format_type == "T20 World Cup": t20wc_analysis.run_t20wc_analysis()

        # ==========================================
        # 3. WOMEN'S LEAGUES
        # ==========================================
        elif category == "Women's Leagues":
            tournament = st.sidebar.selectbox(
                "Select Tournament", 
                ["Women's Premier League (WPL)", "Women's Big Bash League (WBBL)"]
            )
            
            if tournament == "Women's Premier League (WPL)": wpl_analysis.run_wpl_analysis()
            elif tournament == "Women's Big Bash League (WBBL)": wbbl_analysis.run_wbbl_analysis()

        # ==========================================
        # 4. WOMEN'S INTERNATIONAL
        # ==========================================
        elif category == "Women's International":
            format_type = st.sidebar.selectbox(
                "Select Format", 
                ["One Day Internationals", "T20 Internationals", "Tests", "T20 World Cup", "ODI World Cup"]
            )
            
            if format_type == "One Day Internationals": wodi_analysis.run_wodi_analysis()
            elif format_type == "T20 Internationals": wt20i_analysis.run_wt20i_analysis()
            elif format_type == "Tests": wtest_analysis.run_wtest_analysis()
            elif format_type == "T20 World Cup": wt20wc_analysis.run_wt20wc_analysis()
            elif format_type == "ODI World Cup": wodiwc_analysis.run_wodiwc_analysis()

    # ==========================================
    # FOOTBALL SECTION 
    # ==========================================
    elif sport == "Football":
        category = st.sidebar.selectbox(
            "Football Category", 
            ["Domestic Leagues", "Club Continental", "International"]
        )
        
        if category == "Domestic Leagues":
            tournament = st.sidebar.selectbox(
                "Select League", 
                ["English Premier League (EPL)", "La Liga", "Serie A", "Bundesliga", "Ligue 1", "MLS"]
            )
            
            if tournament == "English Premier League (EPL)": epl_analysis.run_epl_analysis()
            elif tournament == "La Liga": laliga_analysis.run_laliga_analysis()
            elif tournament == "Serie A": seriea_analysis.run_seriea_analysis()
            elif tournament == "Bundesliga": bundesliga_analysis.run_bundesliga_analysis()
            elif tournament == "Ligue 1": ligue1_analysis.run_ligue1_analysis()
            elif tournament == "MLS": mls_analysis.run_mls_analysis()
            else:
                st.info(f"The {tournament} dashboard is currently under construction. Booting up ETL pipelines soon...")
                
        elif category in ["Club Continental", "International"]:
             st.info(f"The {category} dashboard is currently under construction.")

if __name__ == "__main__":
    main()