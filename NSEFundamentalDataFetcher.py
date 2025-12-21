import yfinance as yf
import pandas as pd
import time
from typing import List, Dict, Any, Optional

# --- Configuration ---
# NOTE: PEG Ratio and FII Holding are usually NOT available directly via yfinance.
# In a real-world application, you would need to use a dedicated paid API (like Finnhub, Alpha Vantage)
# or a custom scraper for an Indian financial data portal (which can be fragile and against TOS).
# For this script, we use a placeholder function for those metrics.

# Sample list of Nifty 50 stocks (use .NS suffix for NSE)
NSE_TICKERS: List[str] = [
    "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INFY.NS",
    "HINDUNILVR.NS", "KOTAKBANK.NS", "BHARTIARTL.NS", "SBIN.NS", "MARUTI.NS"
]

def fetch_peg_ratio(ticker: str) -> Optional[float]:
    """
    Placeholder for fetching PEG Ratio.
    This data is generally not available in free Yahoo Finance data for NSE.
    Returns a dummy value for demonstration.
    """
    # In a real script, you would call a dedicated API here.
    # For demonstration, we simulate data:
    if ticker in ["RELIANCE.NS", "TCS.NS"]:
        return round(1.2 + (hash(ticker) % 100) / 1000, 2)
    return round(0.5 + (hash(ticker) % 100) / 1000, 2)

def fetch_fii_holding(ticker: str) -> Optional[float]:
    """
    Placeholder for fetching FII Holding percentage.
    This data is specific to Indian market filings and is highly unlikely
    to be available in general international financial APIs.
    Returns a dummy value for demonstration.
    """
    # In a real script, this would require scraping an Indian portal or using a paid API.
    # For demonstration, we simulate data (FII usually holds 10% to 30% in large caps):
    if ticker in ["HDFCBANK.NS", "ICICIBANK.NS"]:
        return round(25.0 + (hash(ticker) % 500) / 100, 2)
    return round(10.0 + (hash(ticker) % 500) / 100, 2)

def fetch_nse_fundamentals(tickers: List[str]) -> pd.DataFrame:
    """
    Fetches P/E ratio via yfinance and simulates PEG/FII data for all tickers.

    Args:
        tickers: A list of NSE stock symbols (e.g., ["TCS.NS", "RELIANCE.NS"]).

    Returns:
        A pandas DataFrame containing the requested fundamental metrics.
    """
    results: List[Dict[str, Any]] = []

    print(f"Starting data fetch for {len(tickers)} tickers...")

    for i, ticker_symbol in enumerate(tickers):
        print(f"({i+1}/{len(tickers)}) Fetching data for {ticker_symbol}...")
        try:
            # Fetch Ticker object
            ticker = yf.Ticker(ticker_symbol)

            # Get general info (P/E is often found here)
            info = ticker.info

            # Extract P/E Ratio (Trailing P/E)
            # Use get() for safe access as keys might be missing
            pe_ratio = info.get('trailingPE')

            # Fetch Placeholder Data for NSE-specific metrics
            peg_ratio = fetch_peg_ratio(ticker_symbol)
            fii_holding = fetch_fii_holding(ticker_symbol)

            results.append({
                'Symbol': ticker_symbol,
                'Company Name': info.get('longName', 'N/A'),
                'P/E Ratio (Trailing)': round(pe_ratio, 2) if pe_ratio else None,
                'PEG Ratio (Simulated)': peg_ratio,
                'FII Holding % (Simulated)': fii_holding
            })

            # Be a good citizen: Wait slightly between requests to avoid rate-limiting
            time.sleep(0.5)

        except Exception as e:
            print(f"Error fetching data for {ticker_symbol}: {e}")
            results.append({
                'Symbol': ticker_symbol,
                'Company Name': 'N/A',
                'P/E Ratio (Trailing)': None,
                'PEG Ratio (Simulated)': None,
                'FII Holding % (Simulated)': None
            })
            time.sleep(0.5) # Still wait on error

    # Convert the list of results into a DataFrame
    df = pd.DataFrame(results)
    return df

# --- Execution ---
if __name__ == "__main__":
    # Fetch the data
    fundamental_data = fetch_nse_fundamentals(NSE_TICKERS)

    # Clean up the output for better readability
    fundamental_data.columns = [
        'Symbol', 'Company Name', 'P/E Ratio',
        'PEG Ratio (Simulated)', 'FII Holding % (Simulated)'
    ]

    # Print results to console
    print("\n--- NSE Stock Fundamental Data ---")
    print(fundamental_data.to_string(index=False))

    # Save to CSV for external analysis
    output_filename = "nse_fundamentals.csv"
    fundamental_data.to_csv(output_filename, index=False)
    print(f"\nData successfully saved to {output_filename}")

    # Example of analysis: filter for low P/E stocks
    low_pe_stocks = fundamental_data[
        (fundamental_data['P/E Ratio'] > 0) &
        (fundamental_data['P/E Ratio'] < 25)
    ].sort_values(by='P/E Ratio')

    print("\n--- Stocks with P/E < 25 ---")
    print(low_pe_stocks[['Symbol', 'P/E Ratio']].to_string(index=False))
