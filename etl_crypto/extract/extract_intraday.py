import requests
import json
from datetime import datetime
from pathlib import Path
from time import sleep

# ==========================
# CONFIG
# ==========================
BASE_URL = "https://api.binance.com/api/v3/klines"
INTERVAL = "1m"   # или "15m"
LIMIT = 1         # берём только последнюю свечу
SLEEP_SECONDS = 0.1

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

# путь к существующей папке intraday
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "crypto_data/raw/intraday"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ==========================
# ФУНКЦИЯ ЗАГРУЗКИ
# ==========================

def fetch_save_intraday(symbol: str):
    params = {
        "symbol": symbol,
        "interval": INTERVAL,
        "limit": LIMIT
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    raw_data = response.json()

    # текущее время запроса
    fetch_time = datetime.utcnow().isoformat()

    wrapped = {
        "symbol": symbol,
        "interval": INTERVAL,
        "timezone": "UTC",
        "fetch_time": fetch_time,
        "rows": len(raw_data),
        "data": raw_data
    }

    # имя файла: символ + timestamp запроса
    timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    symbol_path = DATA_DIR / symbol
    symbol_path.mkdir(parents = True, exist_ok = True)
    file_path = symbol_path / f"{symbol}_{INTERVAL}_{timestamp_str}.json"

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(wrapped, f, indent=2)

    print(f"[SAVED] {symbol} → {file_path}")

# ==========================
# ЦИКЛ ПО ВСЕМ ПАРАМ
# ==========================

for symbol in SYMBOLS:
    try:
        fetch_save_intraday(symbol)
        sleep(SLEEP_SECONDS)
    except Exception as e:
        print(f"[ERROR] {symbol}: {e}")

print("=== ALL DONE ===")