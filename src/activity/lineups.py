import pandas as pd

from definitions import DATA_DIR
from src.util.csv_persistence import read_from_csv


# def get_lineup_by_event_id(game_id, team_id, event_id):
def join_lineup_by_event_id(df_events, df_lineup=None):

    print('-----')
    if df_lineup is None:
        df_lineup = read_from_csv(DATA_DIR + "/tables/Lineups.csv")

    print(len(df_lineup))
    print(len(df_events))
    df = pd.merge(left=df_lineup, right=df_events, how='inner', on=['Game_id', 'Team_id'])
    print(len(df))
    df = df.loc[df['Canonical_Game_Event_Num'] > df['Start_Canonical_Game_Event_Num']]
    df = df.loc[df['Canonical_Game_Event_Num'] < df['End_Canonical_Game_Event_Num']]

    df = groom_columns(df)

    return df

def groom_columns(df):
    COLUMNS = ['Game_id', 'Team_id', 'Start_Canonical_Game_Event_Num', 'Player1', 'Player2', 'Player3', 'Player4', 'Player5', 'End_Canonical_Game_Event_Num', 'Event_Msg_Type', 'Action_Type', 'Num_points', 'Canonical_Game_Event_Num']
    df = df.rename(columns={"Option1": "Num_points"})
    return df[COLUMNS]
