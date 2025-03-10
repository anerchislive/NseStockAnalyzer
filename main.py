import streamlit as st

st.set_page_config(
    page_title="NSE Stock Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.title("NSE Stock Analysis Platform")
    
    st.markdown("""
    Welcome to the NSE Stock Analysis Platform. This tool provides technical analysis and trading signals
    for NSE-listed stocks.
    
    ### Features:
    - Real-time stock data and technical indicators
    - Interactive charts with multiple timeframes
    - Trading signals based on technical analysis
    - Stock screener with customizable criteria
    
    ### Available Tools:
    1. **Stock Analysis**: Detailed technical analysis with multiple indicators
    2. **Stock Screener**: Screen stocks based on technical criteria
    
    Choose a tool from the sidebar to get started.
    """)
    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a Tool", ["Stock Analysis", "Stock Screener"])
    
    if page == "Stock Analysis":
        from pages.stock_analysis import stock_analysis_page
        stock_analysis_page()
    else:
        from pages.stock_screener import stock_screener_page
        stock_screener_page()

if __name__ == "__main__":
    main()
