from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

# Step 1: Launch Chrome
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Step 2: Go to Screener.in login page
print("🔑 Opening Screener.in login page...")
driver.get("https://www.screener.in/login/")

# Step 3: Wait for you to log in
print("Please log in manually in the browser window.")
print("⏳ Waiting 60 seconds... (you can increase if needed)")
time.sleep(60)  # Give yourself time to log in

# Step 4: Extract cookies
cookies = driver.get_cookies()
sessionid = None
for cookie in cookies:
    if cookie['name'] == 'sessionid':
        sessionid = cookie['value']
        break

# Step 5: Save sessionid to file
if sessionid:
    print("\n✅ Session ID found!")
    print(f"sessionid = {sessionid}")

    with open("screener_cookie.json", "w") as f:
        json.dump({"sessionid": sessionid}, f, indent=4)
    print("💾 Saved to screener_cookie.json")

else:
    print("❌ sessionid not found. Please ensure you logged in fully and Screener loaded your dashboard.")

# Step 6: Close browser
driver.quit()
