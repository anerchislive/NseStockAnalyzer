import pandas as pd
import numpy as np

def calculate_sma(data, period=20):
    """Calculate Simple Moving Average."""
    return data.rolling(window=period).mean()

def calculate_ema(data, period=20):
    """Calculate Exponential Moving Average."""
    return data.ewm(span=period, adjust=False).mean()

def calculate_rsi(data, period=14):
    """Calculate Relative Strength Index."""
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def calculate_macd(data):
    """Calculate MACD."""
    exp1 = data.ewm(span=12, adjust=False).mean()
    exp2 = data.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    hist = macd - signal
    return pd.DataFrame({
        'MACD': macd,
        'Signal': signal,
        'Histogram': hist
    })

def calculate_bollinger_bands(data, period=20, num_std=2):
    """Calculate Bollinger Bands."""
    sma = data.rolling(window=period).mean()
    std = data.rolling(window=period).std()
    upper = sma + (std * num_std)
    lower = sma - (std * num_std)
    return pd.DataFrame({
        'Upper': upper,
        'Middle': sma,
        'Lower': lower
    })

def add_indicators(df):
    """Add all technical indicators to the dataframe."""
    df = df.copy()

    # Calculate indicators
    df['SMA_20'] = calculate_sma(df['Close'], 20)
    df['EMA_20'] = calculate_ema(df['Close'], 20)
    df['RSI'] = calculate_rsi(df['Close'])

    # MACD
    macd_data = calculate_macd(df['Close'])
    df['MACD'] = macd_data['MACD']
    df['MACD_Signal'] = macd_data['Signal']
    df['MACD_Hist'] = macd_data['Histogram']

    # Bollinger Bands
    bbands = calculate_bollinger_bands(df['Close'])
    df['BB_Upper'] = bbands['Upper']
    df['BB_Middle'] = bbands['Middle']
    df['BB_Lower'] = bbands['Lower']

    return df