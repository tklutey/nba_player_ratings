import pandas as pd


def read_from_csv(filepath):
    return pd.read_csv(filepath, index_col=False)

def write_to_csv(df, filepath):
    df.to_csv(filepath)