import pandas as pd

def clean_json(data, columns=None):

    # Если одиночный объект — превращаем в список
    if isinstance(data, dict):
        data = [data]

    df = pd.DataFrame(data)

    # Если колонки не указаны — берем все
    if columns is None:
        columns = df.columns.tolist()

    # Если одно значение — превращаем в список
    if isinstance(columns, str):
        columns = [columns]

    for col in columns:
        if col not in df.columns:
            continue

        # Удалить пробелы
        df[col] = df[col].astype(str).str.strip()

        # Пустые строки -> NA
        df[col] = df[col].replace("", pd.NA)

    return df