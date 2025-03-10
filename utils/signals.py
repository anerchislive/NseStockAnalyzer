import numpy as np
import pandas as pd

def generate_signals(df):
    """Generate trading signals based on technical indicators."""
    signals = pd.DataFrame(index=df.index)
    
    # RSI Signals
    signals['RSI_Signal'] = 'Neutral'
    signals.loc[df['RSI'] < 30, 'RSI_Signal'] = 'Oversold'
    signals.loc[df['RSI'] > 70, 'RSI_Signal'] = 'Overbought'
    
    # MACD Signals
    signals['MACD_Signal'] = 'Neutral'
    signals.loc[df['MACD'] > df['MACD_Signal'], 'MACD_Signal'] = 'Buy'
    signals.loc[df['MACD'] < df['MACD_Signal'], 'MACD_Signal'] = 'Sell'
    
    # Bollinger Bands Signals
    signals['BB_Signal'] = 'Neutral'
    signals.loc[df['Close'] < df['BB_Lower'], 'BB_Signal'] = 'Oversold'
    signals.loc[df['Close'] > df['BB_Upper'], 'BB_Signal'] = 'Overbought'
    
    # Moving Average Signals
    signals['MA_Signal'] = 'Neutral'
    signals.loc[df['Close'] > df['SMA_20'], 'MA_Signal'] = 'Bullish'
    signals.loc[df['Close'] < df['SMA_20'], 'MA_Signal'] = 'Bearish'
    
    return signals

def get_signal_summary(signals):
    """Generate a summary of current signals."""
    latest_signals = signals.iloc[-1]
    
    summary = {
        'RSI': latest_signals['RSI_Signal'],
        'MACD': latest_signals['MACD_Signal'],
        'Bollinger': latest_signals['BB_Signal'],
        'Moving Average': latest_signals['MA_Signal']
    }
    
    # Overall sentiment
    bullish_count = sum(1 for signal in summary.values() if signal in ['Buy', 'Bullish', 'Oversold'])
    bearish_count = sum(1 for signal in summary.values() if signal in ['Sell', 'Bearish', 'Overbought'])
    
    if bullish_count > bearish_count:
        summary['Overall'] = 'Bullish'
    elif bearish_count > bullish_count:
        summary['Overall'] = 'Bearish'
    else:
        summary['Overall'] = 'Neutral'
    
    return summary
