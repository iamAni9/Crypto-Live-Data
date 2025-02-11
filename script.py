import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import time
import schedule
import pandas as pd
import os
import json
from dotenv import load_dotenv

load_dotenv()
# Fetch data from CoinGecko API
def fetch_top_50_cryptos():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch data")
        return None

# Crypto Data Analysis
def analyze_data(data):
    df = pd.DataFrame(data, columns=["name", "symbol", "current_price", "market_cap", "total_volume", "price_change_percentage_24h"])
    
    # Top 5 cryptocurrencies by market cap
    top_5_by_market_cap = df.nlargest(5, "market_cap")[["name", "market_cap"]]
    
    # Average price of top 50 cryptocurrencies
    average_price = df["current_price"].mean()
    
    # Highest and lowest 24-hour price change
    highest_change = df.nlargest(1, "price_change_percentage_24h")[["name", "price_change_percentage_24h"]]
    lowest_change = df.nsmallest(1, "price_change_percentage_24h")[["name", "price_change_percentage_24h"]]
    
    return top_5_by_market_cap, average_price, highest_change, lowest_change

# Update Google Sheets with additional columns
def update_google_sheet():
    # Google Sheets API Authentication
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_json = os.getenv("GOOGLE_CREDENTIALS")
    creds_dict = json.loads(creds_json)
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    # creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)

    sheet = client.open("Cryptocurrency Live Data").sheet1  # Google Sheet name I'm using

    data = fetch_top_50_cryptos()
    if data:
        rows = []
        for crypto in data:
            row = [
                crypto["name"],
                crypto["symbol"],
                crypto["current_price"],
                crypto["market_cap"],
                crypto["total_volume"],
                crypto["price_change_percentage_24h"]
            ]
            rows.append(row)

        top_5_by_market_cap, average_price, highest_change, lowest_change = analyze_data(data)

        additional_columns_header = ["Top 5 Cryptos by Market Cap", "Average Price", "Highest 24h Change", "Lowest 24h Change"]
        additional_columns_data = [
            ", ".join(top_5_by_market_cap["name"].tolist()),
            f"${average_price:.2f}",
            f"{highest_change['name'].values[0]} ({highest_change['price_change_percentage_24h'].values[0]:.2f}%)",
            f"{lowest_change['name'].values[0]} ({lowest_change['price_change_percentage_24h'].values[0]:.2f}%)"
        ]

        headers = ["Name", "Symbol", "Current Price (USD)", "Market Cap", "24h Volume", "24h Price Change (%)"] + additional_columns_header
        combined_data = [headers]  

        for i, row in enumerate(rows):
            if i == 0:
                combined_data.append(row + additional_columns_data)
            else:
                combined_data.append(row + [""] * len(additional_columns_header))  # Empty values for other rows

    
        sheet.clear()
        sheet.update(combined_data)
        
        header_range = "A1:J1"  
        sheet.format(header_range, {
            "textFormat": {
                "bold": True
            }
        })
        
        print("Google Sheet updated at:", time.strftime("%Y-%m-%d %H:%M:%S"))

# Schedule updates every 5 minutes
schedule.every(5).minutes.do(update_google_sheet)

# Initial update
update_google_sheet()

# Run the scheduler
while True:
    schedule.run_pending()
    time.sleep(1)