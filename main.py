import streamlit as st

st.set_page_config(
    page_title="NSE Stock Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS to reduce sidebar width and improve layout
st.markdown("""
<style>
    [data-testid="stSidebar"][aria-expanded="true"] {
        min-width: 200px;
        max-width: 200px;
    }
    [data-testid="stSidebar"][aria-expanded="false"] {
        min-width: 200px;
        margin-left: -200px;
    }
    .css-1d391kg {
        padding-top: 1rem;
    }
    .stApp > header {
        background-color: transparent;
    }
    .news-table {
        font-size: 14px;
        width: 100%;
    }
    .news-table td {
        padding: 8px;
    }
</style>
""", unsafe_allow_html=True)

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
    - Latest news for NSE stocks
    - AI-powered stock recommendations

    ### Available Tools:
    1. **Stock Analysis**: Detailed technical analysis with multiple indicators
    2. **Stock Screener**: Screen stocks based on technical criteria
    3. **AI Recommendations**: Get AI-powered stock recommendations
    4. **News**: Latest news articles for NSE stocks

    Choose a tool from the sidebar to get started.
    """)

    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Select a Tool", 
                           ["Stock Analysis", "Stock Screener", "AI Recommendations", "News"])

    if page == "Stock Analysis":
        from pages.stock_analysis import stock_analysis_page
        stock_analysis_page()
    elif page == "Stock Screener":
        from pages.stock_screener import stock_screener_page
        stock_screener_page()
    elif page == "AI Recommendations":
        from pages.recommendations import recommendations_page
        recommendations_page()
    else:
        from pages.news import news_page
        news_page()

if __name__ == "__main__":
    main()