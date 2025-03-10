import pandas as pd
import numpy as np
from utils.indicators import add_indicators
from utils.signals import generate_signals, get_signal_summary

def calculate_technical_score(df):
    """Calculate technical analysis score based on multiple indicators."""
    score = 0
    latest = df.iloc[-1]
    
    # RSI Analysis (0-100)
    rsi = latest['RSI']
    if rsi < 30:  # Oversold
        score += 20
    elif rsi > 70:  # Overbought
        score -= 20
    else:  # Neutral
        score += 10
    
    # MACD Analysis
    if latest['MACD'] > latest['MACD_Signal']:  # Bullish crossover
        score += 20
    elif latest['MACD'] < latest['MACD_Signal']:  # Bearish crossover
        score -= 20
        
    # Moving Average Analysis
    if latest['Close'] > latest['SMA_20']:  # Above MA
        score += 15
    else:  # Below MA
        score -= 15
        
    # Bollinger Bands Analysis
    if latest['Close'] < latest['BB_Lower']:  # Oversold
        score += 15
    elif latest['Close'] > latest['BB_Upper']:  # Overbought
        score -= 15
        
    # Volume Analysis
    vol_sma = df['Volume'].rolling(window=20).mean().iloc[-1]
    if latest['Volume'] > vol_sma * 1.5:  # High volume
        score += 10
        
    return max(min(score, 100), -100)  # Normalize between -100 and 100

def get_recommendation(score):
    """Convert technical score to recommendation."""
    if score >= 50:
        return 'Strong Buy'
    elif score >= 20:
        return 'Buy'
    elif score <= -50:
        return 'Strong Sell'
    elif score <= -20:
        return 'Sell'
    else:
        return 'Hold'

def get_confidence_level(score):
    """Calculate confidence level based on absolute score."""
    abs_score = abs(score)
    if abs_score >= 70:
        return 'High'
    elif abs_score >= 40:
        return 'Medium'
    else:
        return 'Low'

def analyze_stock(symbol, df):
    """Generate comprehensive stock analysis and recommendation."""
    try:
        # Add technical indicators
        df = add_indicators(df)
        
        # Generate signals
        signals = generate_signals(df)
        signal_summary = get_signal_summary(signals)
        
        # Calculate technical score
        tech_score = calculate_technical_score(df)
        
        # Generate recommendation
        recommendation = get_recommendation(tech_score)
        confidence = get_confidence_level(tech_score)
        
        return {
            'symbol': symbol,
            'recommendation': recommendation,
            'technical_score': tech_score,
            'confidence': confidence,
            'signal_summary': signal_summary,
            'last_price': df['Close'].iloc[-1],
            'price_change': ((df['Close'].iloc[-1] / df['Close'].iloc[-2]) - 1) * 100
        }
    except Exception as e:
        return None
