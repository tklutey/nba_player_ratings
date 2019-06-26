import pandas as pd

from definitions import DATA_DIR
from src.util.csv_persistence import read_from_csv


def get_matchup_by_game_ids(df_input, df_matchup=None):
    if df_matchup is None:
        df_matchup = read_from_csv(DATA_DIR + "/tables/Matchups.csv")
    df = pd.merge(left=df_input, right=df_matchup, how='inner', on=['Game_id'])
    df = create_side_labels(df)
    return df

def create_side_labels(matchups):
    a = matchups.loc[matchups['Team_id'] == matchups['Team1']].copy()
    a['Off_team'] = a['Team1']
    a['Def_team'] = a['Team2']
    b = matchups.loc[matchups['Team_id'] != matchups['Team1']].copy()
    b['Off_team'] = b['Team2']
    b['Def_team'] = b['Team1']
    c = a.append(b)
    c = groom_columns(c)
    return c

def groom_columns(df):
    df = df.drop(['Team1', 'Team2', 'Team_id'], axis=1)
    return df

