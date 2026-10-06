import pandas as pd

def reader(file_path) -> pd.DataFrame:
    df = pd.read_csv(file_path, engine='python')
    return df