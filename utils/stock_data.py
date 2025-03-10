import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def get_stock_data(symbol, period='1y', interval='1d'):
    """Fetch stock data from yfinance."""
    try:
        # Add .NS suffix for NSE stocks
        ticker = yf.Ticker(f"{symbol}.NS")
        df = ticker.history(period=period, interval=interval)
        
        if df.empty:
            return None, "No data available for this symbol"
        
        return df, None
    except Exception as e:
        return None, f"Error fetching data: {str(e)}"

def get_company_info(symbol):
    """Get company information."""
    try:
        ticker = yf.Ticker(f"{symbol}.NS")
        info = ticker.info
        return {
            'name': info.get('longName', symbol),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 'N/A'),
            'volume': info.get('volume', 'N/A')
        }
    except:
        return {
            'name': symbol,
            'sector': 'N/A',
            'industry': 'N/A',
            'market_cap': 'N/A',
            'volume': 'N/A'
        }

def format_number(number):
    """Format large numbers to readable format."""
    if not isinstance(number, (int, float)) or pd.isna(number):
        return 'N/A'
    
    if number >= 1e9:
        return f'₹{number/1e9:.2f}B'
    elif number >= 1e6:
        return f'₹{number/1e6:.2f}M'
    else:
        return f'₹{number:,.2f}'
