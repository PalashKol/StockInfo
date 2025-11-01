import yfinance as yf
import pandas as pd

# --- Variable Description ---
# symbol: NSE/BSE stock symbol
# years: number of years for EPS growth (for PEG calculation)

symbol = "INFY.NS"  # Example: Infosys Ltd
years = 3

# --- Fetch company data ---
stock = yf.Ticker(symbol)
info = stock.info

# --- Extract basic data ---
pe = info.get("trailingPE")
pb = info.get("priceToBook")
eps = info.get("trailingEps")
roe = info.get("returnOnEquity")
roa = info.get("returnOnAssets")
debt_to_equity = info.get("debtToEquity")
dividend_yield = info.get("dividendYield")
price_to_sales = info.get("priceToSalesTrailing12Months")
market_cap = info.get("marketCap")
total_revenue = info.get("totalRevenue")
net_income = info.get("netIncomeToCommon")

# --- Historical financials ---
bs = stock.balance_sheet
fin = stock.financials
cf = stock.cashflow

# --- Compute derived ratios ---
current_ratio = None
if "Total Current Assets" in bs.index and "Total Current Liabilities" in bs.index:
    current_assets = bs.loc["Total Current Assets"].iloc[0]
    current_liabilities = bs.loc["Total Current Liabilities"].iloc[0]
    current_ratio = current_assets / current_liabilities

# Asset Turnover
asset_turnover = None
if total_revenue and "Total Assets" in bs.index:
    total_assets = bs.loc["Total Assets"].iloc[0]
    asset_turnover = total_revenue / total_assets

# EPS growth for PEG
eps_growth = None
peg = None
financials = fin
if "Diluted EPS" in financials.index and financials.shape[1] > 1:
    latest_eps = financials.loc["Diluted EPS"].iloc[0]
    old_eps = financials.loc["Diluted EPS"].iloc[min(years - 1, financials.shape[1] - 1)]
    if old_eps and old_eps != 0:
        eps_growth = ((latest_eps - old_eps) / abs(old_eps)) * 100
        if pe and eps_growth != 0:
            peg = pe / eps_growth

# --- Build DataFrame for display ---
ratios = {
    "P/E Ratio": pe,
    "P/B Ratio": pb,
    "PEG Ratio": peg,
    "EPS (TTM)": eps,
    "ROE": roe,
    "ROA": roa,
    "Debt to Equity": debt_to_equity,
    "Dividend Yield": dividend_yield,
    "Price to Sales": price_to_sales,
    "Market Cap": market_cap,
    "Net Profit Margin": (net_income / total_revenue) if (net_income and total_revenue) else None,
    "Current Ratio": current_ratio,
    "Asset Turnover": asset_turnover
}

df = pd.DataFrame(ratios.items(), columns=["Ratio", "Value"])
print(f"\n📊 Fundamental Ratios for {symbol}\n")
print(df.to_string(index=False))
