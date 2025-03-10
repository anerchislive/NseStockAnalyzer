import streamlit as st
import feedparser
import pandas as pd
from datetime import datetime
from urllib.parse import quote

def fetch_stock_news(symbol):
    """Fetch news for a specific stock symbol."""
    query = f"{symbol} NSE stock"
    encoded_query = quote(query)
    feed_url = f"https://news.google.com/rss/search?q={encoded_query}&hl=en-IN&gl=IN&ceid=IN:en"
    
    try:
        feed = feedparser.parse(feed_url)
        news_items = []
        
        for entry in feed.entries[:5]:  # Get top 5 news items per stock
            news_items.append({
                'Symbol': symbol,
                'Title': entry.title,
                'Link': entry.link,
                'Published': datetime.strptime(entry.published, '%a, %d %b %Y %H:%M:%S %Z'),
                'Source': entry.source.title if hasattr(entry, 'source') else 'Unknown'
            })
        
        return news_items
    except Exception as e:
        st.error(f"Error fetching news for {symbol}: {str(e)}")
        return []

def news_page():
    st.title("NSE Stocks News")
    
    try:
        # Read symbols from CSV
        symbols = pd.read_csv("attached_assets/symbol.csv", names=['Symbol'], skiprows=1)
        symbols_list = symbols['Symbol'].dropna().tolist()
        
        # Fetch news for all symbols
        with st.spinner("Fetching latest news..."):
            all_news = []
            for symbol in symbols_list:
                all_news.extend(fetch_stock_news(symbol))
            
            # Sort news by publication date
            all_news.sort(key=lambda x: x['Published'], reverse=True)
            
            # Create DataFrame for display
            news_df = pd.DataFrame(all_news)
            
            # Format the table
            if not news_df.empty:
                # Convert datetime to string for display
                news_df['Published'] = news_df['Published'].dt.strftime('%Y-%m-%d %H:%M')
                
                # Create clickable links
                news_df['Title'] = news_df.apply(
                    lambda row: f'<a href="{row["Link"]}" target="_blank">{row["Title"]}</a>', 
                    axis=1
                )
                
                # Display the table with HTML
                st.markdown("""
                <style>
                .news-table {
                    font-size: 14px;
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown(
                    news_df[['Published', 'Symbol', 'Title', 'Source']]
                    .to_html(escape=False, index=False, classes='news-table'),
                    unsafe_allow_html=True
                )
            else:
                st.info("No news articles found.")
                
    except Exception as e:
        st.error(f"Error loading news: {str(e)}")

if __name__ == "__main__":
    news_page()
