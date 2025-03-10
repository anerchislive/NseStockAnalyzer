import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

from utils.stock_data import get_stock_data, get_company_info, format_number
from utils.indicators import add_indicators
from utils.signals import generate_signals, get_signal_summary

def plot_stock_data(df, signals):
    """Create interactive stock charts with indicators."""
    fig = make_subplots(rows=3, cols=1, 
                        shared_xaxes=True,
                        vertical_spacing=0.05,
                        row_heights=[0.6, 0.2, 0.2])

    # Candlestick chart
    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='OHLC'
    ), row=1, col=1)

    # Add indicators
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20', line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper', line=dict(color='gray', dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower', line=dict(color='gray', dash='dash')), row=1, col=1)

    # MACD
    fig.add_trace(go.Bar(x=df.index, y=df['MACD_Hist'], name='MACD Hist'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['MACD_Signal'], name='MACD Signal'), row=2, col=1)

    # RSI
    fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI'), row=3, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

    # Update layout
    fig.update_layout(
        height=800,
        xaxis_rangeslider_visible=False,
        template='plotly_white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )

    # Update y-axis titles
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="MACD", row=2, col=1)
    fig.update_yaxes(title_text="RSI", row=3, col=1)

    return fig

def stock_analysis_page():
    st.title("Stock Technical Analysis")

    # Load symbols from CSV
    try:
        # Read CSV file with no header, then assign column name
        symbols = pd.read_csv("attached_assets/symbol.csv", names=['Symbol'], skiprows=1)
        selected_symbol = st.selectbox("Select Stock", symbols['Symbol'].dropna())
    except Exception as e:
        st.error(f"Error loading symbols: {str(e)}")
        return

    col1, col2, col3 = st.columns(3)
    timeframe = col1.selectbox("Timeframe", ['1mo', '3mo', '6mo', '1y', '2y', '5y'])
    interval = col2.selectbox("Interval", ['1d', '5d', '1wk', '1mo'])

    if col3.button("Analyze"):
        with st.spinner("Fetching data..."):
            df, error = get_stock_data(selected_symbol, timeframe, interval)

            if error:
                st.error(error)
                return

            # Get company info
            info = get_company_info(selected_symbol)

            # Display company info
            st.subheader(info['name'])
            cols = st.columns(4)
            cols[0].metric("Sector", info['sector'])
            cols[1].metric("Industry", info['industry'])
            cols[2].metric("Market Cap", format_number(info['market_cap']))
            cols[3].metric("Volume", format_number(info['volume']))

            # Calculate indicators and signals
            df = add_indicators(df)
            signals = generate_signals(df)

            # Plot charts
            st.plotly_chart(plot_stock_data(df, signals), use_container_width=True)

            # Display signals
            st.subheader("Trading Signals")
            signal_summary = get_signal_summary(signals)

            signal_cols = st.columns(5)
            for i, (indicator, signal) in enumerate(signal_summary.items()):
                color = "green" if signal in ['Buy', 'Bullish', 'Oversold'] else "red" if signal in ['Sell', 'Bearish', 'Overbought'] else "gray"
                signal_cols[i].markdown(f"**{indicator}**")
                signal_cols[i].markdown(f"<p style='color: {color}'>{signal}</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    stock_analysis_page()