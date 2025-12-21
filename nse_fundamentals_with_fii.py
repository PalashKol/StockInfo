import time
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# ========== CONFIG ==========
NSE_BASE_URL = "https://www.nseindia.com/api/quote-equity?symbol="
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept-Language": "en-US,en;q=0.9",
}

# Load cookie if available
try:
    with open("nse_cookie.json", "r") as f:
        cookie = json.load(f)
        print(f"✅ Using saved cookie: {cookie}")
except FileNotFoundError:
    cookie = {}
    print("⚠️ No saved cookie found. Some NSE data may not load correctly.")


# ========== FUNCTIONS ==========
def get_nse_data(symbol):
    """Fetches EPS, P/E, etc. from NSE"""
    try:
        url = NSE_BASE_URL + symbol
        response = requests.get(url, headers=HEADERS, cookies=cookie, timeout=10)
        response.raise_for_status()
        data = response.json()
        info = data["priceInfo"]

        return {
            "Symbol": symbol,
            "P/E": info.get("pE", None),
            "EPS (TTM)": info.get("eps", None),
        }
    except Exception as e:
        print(f"❌ NSE fetch failed for {symbol}: {e}")
        return {"Symbol": symbol, "P/E": None, "EPS (TTM)": None}


def get_screener_data(symbol):
    """Scrapes PEG ratio, intrinsic value, FII holdings from Screener.in"""
    try:
        url = f"https://www.screener.in/company/{symbol}/"
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        data = {
            "PEG Ratio": None,
            "Debt/Equity": None,
            "Promoter Holding (%)": None,
            "FII Holding (%)": None,
            "Intrinsic Value": None,
        }

        # Key ratios
        for row in soup.select("li.flex.flex-space-between"):
            key = row.find("span", class_="name")
            val = row.find("span", class_="value")
            if not key or not val:
                continue
            key_text = key.text.strip()
            val_text = val.text.strip()

            if "PEG" in key_text:
                data["PEG Ratio"] = val_text
            elif "Debt to equity" in key_text:
                data["Debt/Equity"] = val_text

        # Shareholding pattern
        shareholding = soup.find_all("td", class_="text")
        for cell in shareholding:
            txt = cell.text.strip()
            if "Promoters" in txt:
                data["Promoter Holding (%)"] = cell.find_next("td").text.strip()
            elif "FIIs" in txt:
                data["FII Holding (%)"] = cell.find_next("td").text.strip()

        # Intrinsic value (appears in key metrics table sometimes)
        table_cells = soup.select("td, span")
        for cell in table_cells:
            if "Intrinsic Value" in cell.text:
                data["Intrinsic Value"] = cell.find_next("td").text.strip()
                break

        return data
    except Exception as e:
        print(f"❌ Screener fetch failed for {symbol}: {e}")
        return {
            "PEG Ratio": None,
            "Debt/Equity": None,
            "Promoter Holding (%)": None,
            "FII Holding (%)": None,
            "Intrinsic Value": None,
        }


# ========== MAIN EXECUTION ==========
symbols = ["INFY", "RELIANCE", "TCS"]
results = []

print("\n📊 Advanced Fundamental Analysis (Dynamic - NSE + Screener)\n")

for symbol in symbols:
    print(f"📈 Fetching data for {symbol}...")
    nse_data = get_nse_data(symbol)
    screener_data = get_screener_data(symbol)
    merged = {**nse_data, **screener_data}
    results.append(merged)
    time.sleep(2)

# Convert to DataFrame
df = pd.DataFrame(results)
print(df)

# Save to CSV
df.to_csv("nse_fundamentals_with_fii.csv", index=False)
print("💾 Saved to nse_fundamentals_with_fii.csv")
