import pandas as pd


def process(df, suffix):
    suffix = '_' + suffix
    x = pd.DataFrame()
    for i in range(1, 5+1):
        key = "Player" + str(i)
        y = df[[key, 'Actualized_points']]
        y = y.rename(columns={key: "Player"})
        y = y.rename(columns={'Actualized_points': "Actualized_points" + suffix})

        x = x.append(y)
    x['Possessions' + suffix] = 1
    x = x.groupby(['Player'], as_index=False).sum()
    return x

if __name__ == "__main__":
    df = pd.DataFrame({'Player1': [1, 2, 3], 'Player2': [1, 2, 3], 'Player3': [1, 2, 3], 'Player4': [4, 5, 6], 'Player5': [4, 5, 6], 'Num_points': [2, 2, 2]})
    print(process(df, 'offense'))
