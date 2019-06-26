import pandas as pd

from definitions import DATA_DIR
from src.util.csv_persistence import read_from_csv


# def get_lineup_by_event_id(game_id, team_id, event_id):
def join_lineup_by_event_id(df_events, df_lineup=None):

    if df_lineup is None:
        df_lineup = read_from_csv(DATA_DIR + "/tables/Lineups.csv")

    df = pd.merge(left=df_lineup, right=df_events, how='inner', on=['Game_id', 'Team_id'])
    df = df.loc[df['Canonical_Game_Event_Num'] > df['Start_Canonical_Game_Event_Num']]
    df = df.loc[df['Canonical_Game_Event_Num'] < df['End_Canonical_Game_Event_Num']]

    return df
