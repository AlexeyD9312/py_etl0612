from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
from pathlib import Path
import requests
import json
from time import sleep

# ==========================
# CONFIG
# ==========================
BASE_URL = "https://api.binance.com/api/v3/klines"
INTERVAL = "1m"   # можно менять на "15m"
LIMIT = 1
SLEEP_SECONDS = 0.1
SYMBOLS = [
    "BTCUSDT","ETHUSDT","BNBUSDT","XRPUSDT","SOLUSDT",
    "ADAUSDT","DOGEUSDT","AVAXUSDT","TRXUSDT","DOTUSDT"
]

# Папка RAW intraday внутри контейнера
DATA_DIR = Path("/opt/airflow/cryptodata/raw/intraday")
DATA_DIR.mkdir(parents=True, exist_ok=True)

# ==========================
# Функция запроса и сохранения JSON
# ==========================
def fetch_intraday():
    for symbol in SYMBOLS:
        try:
            params = {"symbol": symbol, "interval": INTERVAL, "limit": LIMIT}
            response = requests.get(BASE_URL, params=params)
            response.raise_for_status()
            raw_data = response.json()

            fetch_time = datetime.utcnow().isoformat()
            wrapped = {
                "symbol": symbol,
                "interval": INTERVAL,
                "timezone": "UTC",
                "fetch_time": fetch_time,
                "rows": len(raw_data),
                "data": raw_data
            }

            # Папка на символ
            symbol_path = DATA_DIR / symbol
            symbol_path.mkdir(parents=True, exist_ok=True)

            # Имя файла с timestamp
            timestamp_str = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
            file_path = symbol_path / f"{symbol}_{INTERVAL}_{timestamp_str}.json"

            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(wrapped, f, indent=2)

            print(f"[SAVED] {symbol} → {file_path}")
            sleep(SLEEP_SECONDS)
        except Exception as e:
            print(f"[ERROR] {symbol}: {e}")

# ==========================
# DAG
# ==========================
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 12, 16),
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'intraday_fetch',
    default_args=default_args,
    schedule_interval='*/15 * * * *',  # каждые 15 минут
    catchup=False
)

t1 = PythonOperator(
    task_id='fetch_intraday_data',
    python_callable=fetch_intraday,
    dag=dag
)