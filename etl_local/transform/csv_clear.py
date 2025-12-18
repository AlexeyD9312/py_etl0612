import pandas as pd 

def clear_csv(df: pd.DataFrame, columns = None ):
    if columns is None:
        columns = df.columns.tolist()#defoult oll columns in file

    elif isinstance(columns, str):
        columns = [columns]

    for column in columns:
        if df[column].dtype == 'object':#object - type(int,float)
            df[column] = df[column].astype(str).str.strip().replace(['','none','N/A','null'], pd.NA)

    return df 
