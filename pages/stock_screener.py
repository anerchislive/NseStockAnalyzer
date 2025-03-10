import streamlit as st
import pandas as pd
from utils.stock_data import get_stock_data
from utils.indicators import add_indicators
from utils.signals import generate_signals

def screen_stocks(symbols, criteria):
    """Screen stocks based on technical criteria."""
    results = []

    for symbol in symbols:
        df, error = get_stock_data(symbol, period='1mo', interval='1d')
        if error:
            continue

        df = add_indicators(df)
        signals = generate_signals(df)
        latest = df.iloc[-1]
        signal_summary = signals.iloc[-1]

        meets_criteria = True
        for criterion in criteria:
            if criterion == 'RSI_Oversold' and latest['RSI'] >= 30:
                meets_criteria = False
            elif criterion == 'RSI_Overbought' and latest['RSI'] <= 70:
                meets_criteria = False
            elif criterion == 'Above_SMA20' and latest['Close'] <= latest['SMA_20']:
                meets_criteria = False
            elif criterion == 'Below_SMA20' and latest['Close'] >= latest['SMA_20']:
                meets_criteria = False
            elif criterion == 'MACD_Bullish' and signal_summary['MACD_Signal'] != 'Buy':
                meets_criteria = False
            elif criterion == 'MACD_Bearish' and signal_summary['MACD_Signal'] != 'Sell':
                meets_criteria = False

        if meets_criteria:
            results.append({
                'Symbol': symbol,
                'Close': latest['Close'],
                'RSI': latest['RSI'],
                'MACD_Signal': signal_summary['MACD_Signal'],
                'MA_Signal': signal_summary['MA_Signal']
            })

    return pd.DataFrame(results)

def stock_screener_page():
    st.title("Stock Screener")

    # Load symbols
    try:
        # Read CSV file with no header, then assign column name
        symbols = pd.read_csv("attached_assets/symbol.csv", names=['Symbol'], skiprows=1)
        symbols_list = symbols['Symbol'].dropna().tolist()
    except Exception as e:
        st.error(f"Error loading symbols: {str(e)}")
        return

    # Screening criteria
    st.subheader("Select Screening Criteria")

    col1, col2 = st.columns(2)

    criteria = []

    with col1:
        if st.checkbox("RSI Conditions"):
            if st.checkbox("Oversold (RSI < 30)"):
                criteria.append('RSI_Oversold')
            if st.checkbox("Overbought (RSI > 70)"):
                criteria.append('RSI_Overbought')

    with col2:
        if st.checkbox("Moving Average Conditions"):
            if st.checkbox("Price Above SMA20"):
                criteria.append('Above_SMA20')
            if st.checkbox("Price Below SMA20"):
                criteria.append('Below_SMA20')

    if st.checkbox("MACD Conditions"):
        col3, col4 = st.columns(2)
        with col3:
            if st.checkbox("Bullish MACD Crossover"):
                criteria.append('MACD_Bullish')
        with col4:
            if st.checkbox("Bearish MACD Crossover"):
                criteria.append('MACD_Bearish')

    if st.button("Run Screener"):
        if not criteria:
            st.warning("Please select at least one screening criterion")
            return

        with st.spinner("Screening stocks..."):
            results = screen_stocks(symbols_list, criteria)

            if results.empty:
                st.info("No stocks found matching the selected criteria")
            else:
                st.subheader("Screening Results")
                st.dataframe(results.style.format({
                    'Close': '{:.2f}',
                    'RSI': '{:.2f}'
                }))

if __name__ == "__main__":
    stock_screener_page()