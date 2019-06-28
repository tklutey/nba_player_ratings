import pandas as pd


def process(df, suffix):
    suffix = '_' + suffix
    x = pd.DataFrame()
    for i in range(1, 5+1):
        key = "Player" + str(i)
        y = df[[key, 'Actualized_points', 'Game_id']]
        y = y.rename(columns={key: "Player"})
        y = y.rename(columns={'Actualized_points': "Actualized_points" + suffix})

        x = x.append(y)
    x['Possessions' + suffix] = 1
    x = x.groupby(['Player', 'Game_id'], as_index=False).sum()
    return x
