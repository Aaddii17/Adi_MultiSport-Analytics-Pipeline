import streamlit as st

# --- IMPORT ALL MODULES ---
import ipl_analysis
import sa20_analysis
import cpl_analysis
import bbl_analysis
import odi_analysis
import odiwc_analysis  # Restored Men's ODI WC
import t20i_analysis
import t20wc_analysis
import wpl_analysis
import wbbl_analysis
import wt20i_analysis
import wodi_analysis
import wtest_analysis
import wt20wc_analysis
import wodiwc_analysis

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Multi-Sport Analytics",
    page_icon="🏏",
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
            
            if tournament == "IPL":
                ipl_analysis.run_ipl_analysis()
            elif tournament == "SA20":
                sa20_analysis.run_sa20_analysis()
            elif tournament == "Caribbean Premier League":
                cpl_analysis.run_cpl_analysis()
            elif tournament == "Big Bash League":
                bbl_analysis.run_bbl_analysis()

        # ==========================================
        # 2. MEN'S INTERNATIONAL
        # ==========================================
        elif category == "Men's International":
            format_type = st.sidebar.selectbox(
                "Select Format", 
                ["One Day Internationals", "ODI World Cup", "T20 Internationals", "T20 World Cup"]
            )
            
            if format_type == "One Day Internationals":
                odi_analysis.run_odi_analysis()
            elif format_type == "ODI World Cup":
                odiwc_analysis.run_odiwc_analysis()
            elif format_type == "T20 Internationals":
                t20i_analysis.run_t20i_analysis()
            elif format_type == "T20 World Cup":
                t20wc_analysis.run_t20wc_analysis()

        # ==========================================
        # 3. WOMEN'S LEAGUES
        # ==========================================
        elif category == "Women's Leagues":
            tournament = st.sidebar.selectbox(
                "Select Tournament", 
                ["Women's Premier League (WPL)", "Women's Big Bash League (WBBL)"]
            )
            
            if tournament == "Women's Premier League (WPL)":
                wpl_analysis.run_wpl_analysis()
            elif tournament == "Women's Big Bash League (WBBL)":
                wbbl_analysis.run_wbbl_analysis()

        # ==========================================
        # 4. WOMEN'S INTERNATIONAL
        # ==========================================
        elif category == "Women's International":
            format_type = st.sidebar.selectbox(
                "Select Format", 
                ["One Day Internationals", "T20 Internationals", "Tests", "T20 World Cup", "ODI World Cup"]
            )
            
            if format_type == "One Day Internationals":
                wodi_analysis.run_wodi_analysis()
            elif format_type == "T20 Internationals":
                wt20i_analysis.run_wt20i_analysis()
            elif format_type == "Tests":
                wtest_analysis.run_wtest_analysis()
            elif format_type == "T20 World Cup":
                wt20wc_analysis.run_wt20wc_analysis()
            elif format_type == "ODI World Cup":
                wodiwc_analysis.run_wodiwc_analysis()

    # ==========================================
    # FOOTBALL SECTION (PLACEHOLDER)
    # ==========================================
    elif sport == "Football":
        st.title("⚽ Football Analytics Pipeline")
        st.info("The Football dashboard is currently under construction.")

if __name__ == "__main__":
    main()