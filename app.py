import streamlit as st

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AdiSports Analytics", 
    page_icon="⚽", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SECURE IMPORTS ---
# Only importing the modules that have been fully developed and pushed to GitHub
from Cricket import ipl_analysis

# Safely importing the Live Football module based on your folder structure
try:
    from Live import live_football
except ImportError:
    # Fallback in case it was saved in the main directory instead of the Live folder
    try:
        import live_football
    except ImportError:
        live_football = None

def main():
    # --- SIDEBAR NAVIGATION ARCHITECTURE ---
    st.sidebar.title("Navigation")
    sport_choice = st.sidebar.radio(
        "Select Sport", 
        ["Cricket", "Football", "Real-Time Live Center"]
    )

    st.sidebar.markdown("---")

    # ==========================================
    # ROUTING: CRICKET MODULE
    # ==========================================
    if sport_choice == "Cricket":
        st.sidebar.caption("Cricket Category")
        category = st.sidebar.selectbox("Select Category", ["Men's Leagues"], label_visibility="collapsed")
        
        st.sidebar.caption("Select Tournament")
        # Kept the other leagues to show future scope, but routed them safely!
        tournament = st.sidebar.selectbox(
            "Select Tournament", 
            ["IPL", "SA20", "CPL", "BBL", "ODI World Cup", "T20 World Cup"], 
            label_visibility="collapsed"
        )
        
        if tournament == "IPL":
            ipl_analysis.run_ipl_analysis()
        else:
            st.warning(f"🚧 Historical analytics for **{tournament}** are currently under construction. Please select **IPL** from the dropdown.")

    # ==========================================
    # ROUTING: FOOTBALL MODULE
    # ==========================================
    elif sport_choice == "Football":
        st.sidebar.caption("Football Category")
        st.sidebar.selectbox("Select League", ["English Premier League", "La Liga", "Serie A", "Bundesliga"], label_visibility="collapsed")
        
        st.info("🚧 Historical Football Analytics are currently being integrated. Please check out the **Real-Time Live Center** for live football tracking!")

    # ==========================================
    # ROUTING: REAL-TIME LIVE CENTER
    # ==========================================
    elif sport_choice == "Real-Time Live Center":
        st.sidebar.caption("Select Live Stream")
        stream_choice = st.sidebar.selectbox(
            "Select Live Stream", 
            ["Live Football Tracker", "Live Cricket Tracking"], 
            label_visibility="collapsed"
        )
        
        if stream_choice == "Live Football Tracker":
            if live_football:
                live_football.run_live_football()
            else:
                st.error("⚠️ System Error: Could not locate `live_football.py`. Please ensure it is uploaded to your GitHub repository.")
        else:
            st.warning("🚧 The Live Cricket API integration is scheduled for a future update.")

if __name__ == "__main__":
    main()
