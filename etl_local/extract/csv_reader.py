import pandas as pd 
import os


def extract_csv(path: str, sep = ',', encoding = 'utf-8') -> pd.DataFrame:
    return pd.read_csv(path, sep = sep, encoding = encoding)