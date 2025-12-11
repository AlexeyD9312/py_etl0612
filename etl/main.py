from extract.csv_reader import extract_csv
from extract.json_reader import extract_json
from transform.csv_clear import clear_csv
from transform.json_clear import clean_json
from load.csv_load import csv_load 
import pandas as pd 
import os 


needed_keys = ["city_name","state_id","living_square_meters","price_total","created_at","total_square_meters","floor"]

def run_etl():
    df_csv = extract_csv('../local_dirty_data/csv/general_characteristics.csv')
    df_json = extract_json('../local_dirty_data/json/0000_30429057_ID.json', needed_keys = needed_keys)
    
    df_csv = clear_csv(df_csv)


    df_json_clear = clean_json(df_json)

    csv_load(df_csv, '../local_clear_data/csv/general_char_clear.csv')
    csv_load(df_json_clear, '../local_clear_data/json/0000_clear_ID.json')


if __name__ == "__main__":
    run_etl()