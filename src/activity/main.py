import pandas as pd

from definitions import DATA_DIR, MADE_BASKET_EVENT_MSG_TYPE
from src.activity.get_rating import get_rating
from src.activity.lineups import join_lineup_by_event_id
from src.activity.matchups import get_matchup_by_game_ids
from src.activity.score_possession import process
from src.util.csv_persistence import read_from_csv


def process_events():
    df = read_from_csv(DATA_DIR + "/tables/Canonical_Events.csv")
    handle(df)

def handle(df):
    df = get_matchup_by_game_ids(df)
    df = groom_columns(df)
    handle_made_fg(df.loc[df['Event_Msg_Type'] == MADE_BASKET_EVENT_MSG_TYPE])


def handle_made_fg(df):
    df_offense = join_lineup_by_event_id(df.rename(columns={'Off_team':'Team_id'}))
    offense = process(df_offense, 'offense')

    df_defense = join_lineup_by_event_id(df.rename(columns={'Def_team':'Team_id'}))
    defense = process(df_defense, 'defense')

    x = pd.merge(left=offense, right=defense, how='inner', on=['Player'])
    x = get_rating(x)
    print(x)

# get num points, game_id, off_team, def_team, event_id
# get lineup


def groom_columns(df):
    COLUMNS = ['Game_id', 'Event_Msg_Type', 'Action_Type', 'Num_points', 'Off_team', 'Def_team', 'Canonical_Game_Event_Num']
    df = df.rename(columns={"Option1": "Num_points"})
    return df[COLUMNS]


if __name__ == "__main__":
    process_events()


