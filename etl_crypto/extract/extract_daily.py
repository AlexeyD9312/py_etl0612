import requests
import json
from datetime import datetime
from pathlib import Path 
from time import sleep 



BASE_URL = "https://api.binance.com/api/v3/klines"
INTERVAL = "1d"
LIMIT = 365
DATA_DIR = Path("../crypto_data/raw/daily")
DATA_DIR.mkdir(parents = True, exist_ok = True)

SYMBOLS = [
    "BTCUSDT",
    "ETHUSDT",
    "BNBUSDT",
    "XRPUSDT",
    "SOLUSDT",
    "ADAUSDT",
    "DOGEUSDT",
    "AVAXUSDT",
    "TRXUSDT",
    "DOTUSDT"
]

SLEEP_SECONDS = 0.3


def fetch_and_save(symbol:str):
    params = {
        "symbol":symbol,
        "interval": INTERVAL,
        "limit" : LIMIT
    }
    response = requests.get(BASE_URL,params = params)
    response.raise_for_status()
    raw_data = response.json()

    period_start = datetime.utcfromtimestamp(raw_data[0][0] / 1000) 
    period_end = datetime.utcfromtimestamp(raw_data[-1][0] / 1000) 

    wrapped = {
        "symbol" : symbol,
        "interval" : INTERVAL,
        "timezone": "UTC",
        "period_start": period_start.isoformat(),
        "period_end" : period_end.isoformat(),
        "rows" : len(raw_data),
        "data" : raw_data
    }

    symbol_path = DATA_DIR / symbol
    symbol_path.mkdir(parents = True, exist_ok = True)
    file_path = symbol_path / f"{symbol}_{INTERVAL}.json"
    with open(file_path,"w",encoding = "utf_8") as f:
        json.dump(wrapped,f,indent = 2)

    print(f"[SAVED] {symbol} → {file_path} ({len(raw_data)} rows)")

# ==========================
# ЦИКЛ ПО ВСЕМ ПАРАМ
# ==========================

for symbol in SYMBOLS:
    try:
        fetch_and_save(symbol)
        sleep(SLEEP_SECONDS)
    except Exception as e:
        print(f"[ERROR] {symbol}: {e}")

print("=== ALL DONE ===")

    
