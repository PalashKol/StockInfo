# File: fundamental_analysis_nse.py
# Description: Fetches key financial & valuation data for NSE-listed companies
# Input: List of NSE stock symbols
# Output: Summary table + details for deeper analysis

import yfinance as yf
import pandas as pd

# List of NSE symbols (append .NS for Yahoo)
symbols = ["INFY.NS", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]

fundamentals = []

for sym in symbols:
    stock = yf.Ticker(sym)
    info = stock.info
    print(info)

    fundamentals.append({
        "Symbol": sym.replace(".NS", ""),
        "Company": info.get("longName"),
        "Sector": info.get("sector"),
        "Market Cap (₹ Cr)": round(info.get("marketCap", 0) / 1e7, 2) if info.get("marketCap") else None,
        "P/E Ratio": info.get("trailingPE"),
        "P/B Ratio": info.get("priceToBook"),
        "EPS (₹)": info.get("trailingEps"),
        "ROE (%)": info.get("returnOnEquity"),
        "ROA (%)": info.get("returnOnAssets"),
        "Dividend Yield (%)": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else 0,
        "Debt to Equity": info.get("debtToEquity"),
        "52W High": info.get("fiftyTwoWeekHigh"),
        "52W Low": info.get("fiftyTwoWeekLow"),
        "Current Price": info.get("currentPrice"),
        "Book Value": info.get("bookValue"),
        "Profit Margin (%)": info.get("profitMargins", 0) * 100 if info.get("profitMargins") else None,
        "Revenue (₹ Cr)": round(info.get("totalRevenue", 0) / 1e7, 2) if info.get("totalRevenue") else None
    })

# Convert to DataFrame
df = pd.DataFrame(fundamentals)

# Display summary
print("\n📊 Fundamental Analysis Summary (NSE Stocks)\n")
print(df.to_string(index=False))

# Save results
df.to_csv("nse_fundamentals.csv", index=False)
print("\n💾 Saved to nse_fundamentals.csv")
