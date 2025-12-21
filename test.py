#Stock/equity information from NSE
import requests

headers = {
    'User-Agent': 'Mozilla/5.0'
}
response = requests.get("https://www.nseindia.com/api/quote-equity?symbol=TCS", headers=headers)
print(response.json())
