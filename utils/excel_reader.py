import pandas as pd

def parse_excel(file_path: str):
    df = pd.read_excel(file_path)
    df = df.fillna("")
    return df.to_dict(orient="records")
