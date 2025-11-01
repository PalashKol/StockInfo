import requests
import pandas as pd
import yfinance as yf
import time
from datetime import datetime

# -------------------------------------------------------
# Step 1 — Get all NSE equity symbols (exclude indices/ETFs)
# -------------------------------------------------------
def get_nse_equity_symbols():
    import pandas as pd
    import io
    import requests

    url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"
    response = requests.get(url)
    response.raise_for_status()

    # Load CSV and clean column names
    df = pd.read_csv(io.StringIO(response.text))
    df.columns = [c.strip().upper() for c in df.columns]

    # Check available columns
    # print(df.columns.tolist())  # uncomment to inspect structure

    # Filter for EQ series only (equity shares)
    if "SERIES" in df.columns:
        df = df[df["SERIES"].str.strip().eq("EQ")]
    elif " SERIES" in df.columns:
        df = df[df[" SERIES"].str.strip().eq("EQ")]
    else:
        raise Exception(f"⚠️ Unexpected columns in NSE CSV: {df.columns.tolist()}")

    symbols = [s.strip() + ".NS" for s in df["SYMBOL"]]
    print(f"✅ Found {len(symbols)} NSE equity shares (from EQUITY_L.csv)")
    return symbols





# -------------------------------------------------------
# Step 2 — Fetch all available ratios for each company
# -------------------------------------------------------
def fetch_ratios(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # Extract all publicly available ratios
        pe = info.get("trailingPE")
        pb = info.get("priceToBook")
        roe = info.get("returnOnEquity")
        roe = roe * 100 if roe else None
        debt_equity = info.get("debtToEquity")
        div_yield = info.get("dividendYield")
        div_yield = div_yield * 100 if div_yield else None
        ps = info.get("priceToSalesTrailing12Months")
        peg = info.get("pegRatio")
        growth = info.get("earningsQuarterlyGrowth")

        # Compute PEG manually if missing
        if not peg and pe and growth and growth != 0:
            peg = pe / (growth * 100)

        return {
            "Symbol": symbol.replace(".NS", ""),
            "Company": info.get("shortName"),
            "Sector": info.get("sector"),
            "Industry": info.get("industry"),
            "P/E": pe,
            "P/B": pb,
            "ROE (%)": roe,
            "Debt/Equity": debt_equity,
            "Dividend Yield (%)": div_yield,
            "Price/Sales": ps,
            "PEG": peg,
            "Market Cap": info.get("marketCap"),
            "52W High": info.get("fiftyTwoWeekHigh"),
            "52W Low": info.get("fiftyTwoWeekLow"),
            "Beta": info.get("beta"),
        }

    except Exception as e:
        print(f"⚠️ Error fetching {symbol}: {e}")
        return None


# -------------------------------------------------------
# Step 3 — Main driver with batch saving
# -------------------------------------------------------
def main():
    symbols = get_nse_equity_symbols()

    batch_size = 50
    all_data = []
    file_name = f"NSE_Equity_Ratios_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"

    for i in range(0, len(symbols), batch_size):
        batch = symbols[i:i + batch_size]
        print(f"\n📦 Processing batch {i//batch_size + 1} / {len(symbols)//batch_size + 1} ...")

        for symbol in batch:
            data = fetch_ratios(symbol)
            if data:
                all_data.append(data)
            time.sleep(0.5)  # avoid hitting Yahoo API too quickly

        # Save partial progress
        pd.DataFrame(all_data).to_excel(file_name, index=False)
        print(f"💾 Saved {len(all_data)} records so far → {file_name}")

    print(f"\n✅ Completed. Total companies processed: {len(all_data)}")
    print(f"📁 Final file saved as: {file_name}")


if __name__ == "__main__":
    main()
