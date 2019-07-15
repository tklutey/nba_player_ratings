import pandas as pd

import definitions
from definitions import RAW_DATA_DIR, DATA_DIR
from src.activity import matchups
from src.util.csv_persistence import read_from_csv, write_to_csv


def main():
    df = read_from_csv(RAW_DATA_DIR + "/csv/Play_by_Play.csv")
    df = mirror_period_end(df)
    df = create_canonical_event_number(df)
    write_to_csv(df, DATA_DIR + "/tables/Canonical_Events.csv")


def create_canonical_event_number(dataframe):
    df = dataframe.groupby('Game_id').apply(create_game_event_number)
    df = df.reset_index(drop=True)
    df = df.rename(columns={"Option1": "Attempted_points"})
    return df


def create_game_event_number(x):
    df_sorted = x.sort_values(by=['Period', 'PC_Time', 'WC_Time', 'Event_Num'],
                              ascending=[True, False, True, True])

    df_sorted = df_sorted.reset_index(drop=True)
    df_sorted['Canonical_Game_Event_Num'] = df_sorted.index

    df_sorted = df_sorted.drop('Event_Num', axis=1)

    return df_sorted


def mirror_period_end(df_canonical):
    df = matchups.get_matchup_by_game_ids(df_canonical)
    df = df.loc[df['Event_Msg_Type'] == definitions.END_OF_PERIOD_EVENT_MSG_TYPE]
    df = df.drop(labels=['Off_team'], axis=1)
    df = df.rename(columns={"Def_team": "Team_id"})

    df = df.append(df_canonical, sort=True)

    return df


if __name__ == "__main__":
    main()
