import streamlit as st
import pandas as pd
from utils.stock_data import get_stock_data, format_number
from utils.recommendation_engine import analyze_stock

def recommendations_page():
    st.title("AI Stock Recommendations")

    # Load symbols
    try:
        symbols = pd.read_csv("attached_assets/symbol.csv", names=['Symbol'], skiprows=1)
        symbols_list = symbols['Symbol'].dropna().tolist()
    except Exception as e:
        st.error(f"Error loading symbols: {str(e)}")
        return

    # Analysis parameters
    min_confidence = st.selectbox("Minimum Confidence Level", ["Low", "Medium", "High"])

    if st.button("Generate Recommendations"):
        with st.spinner("Analyzing all NSE stocks..."):
            recommendations = []

            # Progress bar for analysis
            progress_bar = st.progress(0)
            total_stocks = len(symbols_list)

            # Analyze each stock
            for idx, symbol in enumerate(symbols_list):
                df, error = get_stock_data(symbol, period='3mo', interval='1d')
                if error:
                    continue

                analysis = analyze_stock(symbol, df)
                if analysis:
                    recommendations.append(analysis)

                # Update progress
                progress_bar.progress((idx + 1) / total_stocks)

            if recommendations:
                # Convert to DataFrame
                rec_df = pd.DataFrame(recommendations)

                # Filter by confidence
                confidence_levels = {'Low': 0, 'Medium': 1, 'High': 2}
                min_conf_level = confidence_levels[min_confidence]
                rec_df = rec_df[rec_df['confidence'].map(lambda x: confidence_levels[x]) >= min_conf_level]

                # Sort by technical score
                rec_df = rec_df.sort_values('technical_score', ascending=False)

                # Display recommendations
                st.subheader("Stock Recommendations")

                # Format DataFrame for display
                display_df = rec_df.copy()
                display_df['price_change'] = display_df['price_change'].round(2).astype(str) + '%'
                display_df['technical_score'] = display_df['technical_score'].round(2)

                # Add recommendation basis column
                def get_recommendation_basis(row):
                    signals = []
                    if row['technical_score'] > 50:
                        signals.append("Strong technical indicators")
                    if row['signal_summary']['RSI'] == 'Oversold':
                        signals.append("Oversold (RSI)")
                    if row['signal_summary']['MACD'] == 'Buy':
                        signals.append("Bullish MACD crossover")
                    if row['signal_summary']['Moving Average'] == 'Bullish':
                        signals.append("Above key moving averages")
                    return ", ".join(signals) if signals else "Multiple factors"

                display_df['Basis'] = display_df.apply(get_recommendation_basis, axis=1)

                # Color-code recommendations
                def color_recommendations(val):
                    if 'Strong Buy' in val:
                        return 'background-color: #9fff9c'
                    elif 'Buy' in val:
                        return 'background-color: #c8ffc6'
                    elif 'Strong Sell' in val:
                        return 'background-color: #ffc6c6'
                    elif 'Sell' in val:
                        return 'background-color: #ffdede'
                    return ''

                # Display styled table
                st.dataframe(
                    display_df[['symbol', 'recommendation', 'confidence', 'technical_score', 
                              'price_change', 'last_price', 'Basis']]
                    .style
                    .apply(lambda x: [color_recommendations(val) for val in x], axis=1, subset=['recommendation'])
                    .format({'last_price': '₹{:.2f}'})
                )

                # Display analysis insights
                st.subheader("Analysis Insights")
                total_analyzed = len(recommendations)
                buy_signals = len(rec_df[rec_df['recommendation'].isin(['Buy', 'Strong Buy'])])
                sell_signals = len(rec_df[rec_df['recommendation'].isin(['Sell', 'Strong Sell'])])

                col1, col2, col3 = st.columns(3)
                col1.metric("Total Stocks Analyzed", total_analyzed)
                col2.metric("Buy Signals", buy_signals)
                col3.metric("Sell Signals", sell_signals)

                # Display market sentiment
                st.subheader("Market Sentiment")
                buy_percentage = (buy_signals / total_analyzed) * 100
                if buy_percentage > 60:
                    sentiment = "Bullish"
                    color = "green"
                elif buy_percentage < 40:
                    sentiment = "Bearish"
                    color = "red"
                else:
                    sentiment = "Neutral"
                    color = "gray"

                st.markdown(f"Overall Market Sentiment: <span style='color: {color}'>{sentiment}</span>", 
                          unsafe_allow_html=True)

            else:
                st.warning("No recommendations generated. Please try with different parameters.")

if __name__ == "__main__":
    recommendations_page()