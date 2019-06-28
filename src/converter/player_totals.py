import pandas as pd

from src.activity.lineups import join_lineup_by_event_id
from src.activity.score_possession import process


def get_player_points(df):
    df_offense = join_lineup_by_event_id(df.rename(columns={'Off_team': 'Team_id'}))
    offense = process(df_offense, 'offense')

    df_defense = join_lineup_by_event_id(df.rename(columns={'Def_team': 'Team_id'}))
    defense = process(df_defense, 'defense')

    x = pd.merge(left=offense, right=defense, how='inner', on=['Player', 'Game_id'])
    return x
