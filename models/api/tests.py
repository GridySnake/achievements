import pandas as pd


def test_result(email: str, url: str, percentage: int = None):
    try:
        df = pd.read_csv(url)
        df = df[[i for i in df.columns[0:3]]]
        df = df.loc[df[df.columns[1]] == email]
        df = df.sort_values(df.columns[0])
        if percentage:
            result = int(df[df.columns[2]].iloc[0].split(' / ')[0]) / int(df[df.columns[2]].iloc[0].split(' / ')[1]) * 100
        else:
            result = int(df[df.columns[2]].iloc[0].split(' / ')[0])
    except:
        result = None
    return result
