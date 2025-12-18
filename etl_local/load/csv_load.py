def csv_load(df, path:str):
    df.to_csv(path, index = False)
