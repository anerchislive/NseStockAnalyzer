# NSE Stock Analysis Platform 📈

A comprehensive NSE stock analysis platform built with Streamlit, providing real-time technical indicators, trading signals, and news insights for investors.

## Features

- **Real-time Stock Analysis**: Technical indicators and interactive charts
- **AI-Powered Recommendations**: Smart stock recommendations based on technical analysis
- **Stock Screener**: Filter stocks based on custom technical criteria
- **Live News Feed**: Latest news for NSE stocks using Google News RSS
- **Interactive Charts**: Multi-timeframe analysis with various technical indicators

## Technical Stack

- **Frontend**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Technical Analysis**: Custom implementations of technical indicators
- **Data Source**: yfinance API
- **News Feed**: Google News RSS
- **Visualization**: Plotly

## Dependencies

```txt
streamlit
pandas
numpy
plotly
yfinance
feedparser
pytz
```

## Deployment on Hugging Face Spaces

1. Create a new Space on Hugging Face:
   - Go to huggingface.co/spaces
   - Click "Create new Space"
   - Select "Streamlit" as the SDK
   - Choose a name for your space

2. Upload the Project Files:
   - Upload all project files to your Space
   - Ensure the file structure matches the repository

3. Configure Environment:
   - The platform will automatically install dependencies
   - The app will run on the default Streamlit port

4. Access Your App:
   - Once deployed, your app will be available at: https://huggingface.co/spaces/[USERNAME]/[SPACE-NAME]

## Usage

1. **Stock Analysis**:
   - Select a stock from the dropdown
   - Choose timeframe and interval
   - View technical indicators and signals

2. **Stock Screener**:
   - Set your screening criteria
   - Get filtered results based on technical indicators

3. **AI Recommendations**:
   - View AI-generated stock recommendations
   - Check confidence levels and recommendation basis

4. **News Feed**:
   - Access latest news for all NSE stocks
   - Click on news titles to read full articles

## Local Development

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `streamlit run main.py`
4. Access at: `http://localhost:5000`

## License

This project is licensed under the MIT License - see the LICENSE file for details.
