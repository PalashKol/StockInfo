# File: nse_fundamentals_with_screener.py
# Description: Fetch advanced fundamentals and ownership (FII/DII/Promoter) for NSE stocks

import requests
import yfinance as yf
import pandas as pd

# -------------------------------
# 🔐 Add your Screener cookie here
# -------------------------------
SCREENER_COOKIE = "d765gh3g2mihc4aztrx4mq8peo4uz6im"  # Replace with your sessionid

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Cookie": f"sessionid={SCREENER_COOKIE}"
}

def get_ownership_data(symbol):
    """
    Fetches shareholding pattern data from Screener.in
    """
    try:
        url = f"https://www.screener.in/company/{symbol}/consolidated/"
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.raise_for_status()

        data = {}
        lines = r.text.splitlines()
        for i, line in enumerate(lines):
            if "Promoters" in line:
                data["Promoter (%)"] = lines[i + 1].strip().split()[0].replace("%", "")
            if "Foreign Institutions" in line or "FII" in line:
                data["FII (%)"] = lines[i + 1].strip().split()[0].replace("%", "")
            if "Domestic Institutions" in line or "DII" in line:
                data["DII (%)"] = lines[i + 1].strip().split()[0].replace("%", "")
            if "Public" in line and "Shareholding" not in line:
                data["Public (%)"] = lines[i + 1].strip().split()[0].replace("%", "")
        return data
    except Exception as e:
        print(f"⚠️ Error fetching ownership for {symbol}: {e}")
        return {}

def get_fundamental_data(symbol):
    """
    Fetches key fundamentals from Yahoo Finance
    """
    ticker = yf.Ticker(symbol + ".NS")
    info = ticker.info
    pe = info.get("trailingPE")
    growth = info.get("earningsGrowth")
    eps = info.get("trailingEps")
    price = info.get("currentPrice")

    peg = round(pe / growth, 2) if pe and growth and growth != 0 else None
    intrinsic = round(eps * (8.5 + 2 * ((growth or 0.1) * 100)), 2) if eps else None

    return {
        "Company": info.get("longName"),
        "Sector": info.get("sector"),
        "P/E": pe,
        "Earnings Growth": growth,
        "PEG": peg,
        "Intrinsic Value": intrinsic,
        "Current Price": price,
    }

# -------------------------------
# 🔍 Symbols to analyze
# -------------------------------
symbols = ["INFY", "RELIANCE", "TCS"]

results = []
for sym in symbols:
    fundamentals = get_fundamental_data(sym)
    ownership = get_ownership_data(sym)
    results.append({
        "Symbol": sym,
        **fundamentals,
        **ownership
    })

# -------------------------------
# 💾 Output
# -------------------------------
df = pd.DataFrame(results)
print("\n📊 NSE Fundamental + Ownership Analysis\n")
print(df.to_string(index=False))
df.to_csv("nse_fundamentals_with_ownership.csv", index=False)
print("\n💾 Saved to nse_fundamentals_with_ownership.csv")
