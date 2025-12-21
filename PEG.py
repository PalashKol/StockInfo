
import yfinance as yf

# --- Variable Descriptions ---
# symbol: NSE/BSE stock symbol (use .NS for NSE stocks in Yahoo Finance)
# years: number of years used for EPS growth comparison

symbol = "RELIANCE.NS"  # Example: Reliance Industries
years = 3               # 3-year EPS growth

# --- Fetch data ---
stock = yf.Ticker(symbol)
info = stock.info

# --- Extract data ---
pe_ratio = info.get("trailingPE")
eps_ttm = info.get("trailingEps")

# --- Historical EPS for growth ---
# Fetch annual income statements for EPS comparison
financials = stock.financials
eps_history = financials.loc["Diluted EPS"] if "Diluted EPS" in financials.index else None

if eps_history is not None and eps_history.size >= 2:
    latest_eps = eps_history.iloc[0]
    old_eps = eps_history.iloc[min(years - 1, len(eps_history) - 1)]
    eps_growth = ((latest_eps - old_eps) / old_eps) * 100
else:
    eps_growth = None

# --- Compute PEG ---
if pe_ratio and eps_growth and eps_growth != 0:
    peg_ratio = pe_ratio / eps_growth
    print(f"Company: {symbol}")
    print(f"P/E Ratio: {pe_ratio:.2f}")
    print(f"EPS Growth ({years}Y): {eps_growth:.2f}%")
    print(f"PEG Ratio: {peg_ratio:.2f}")
else:
    print("⚠️ Unable to compute PEG ratio (missing data)")
