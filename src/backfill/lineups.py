import pandas as pd

import definitions
from src.util.csv_persistence import read_from_csv, write_to_csv

GAME_LINEUP_DATA = "/csv/Game_Lineup.csv"


def main():
    df = read_from_csv(definitions.RAW_DATA_DIR + GAME_LINEUP_DATA)
    df_lineups = get_period_starting_lineups(df)
    df_lineups = apply_subs(df_lineups)
    write_to_csv(df_lineups, definitions.DATA_DIR + "/tables/Lineups.csv")


def apply_subs(df_lineups):
    df = read_from_csv(definitions.DATA_DIR + "/tables/Canonical_Events.csv")
    game_ids = df['Game_id'].unique()
    for game_id in game_ids:
        x = df.loc[df['Game_id'] == game_id]
        team_ids = x['Team_id'].unique()
        for team_id in team_ids:
            y = x.loc[x['Team_id'] == team_id]
            for period in range(1, 4 + 1):
                z = y.loc[y['Period'] == period]
                z = z.loc[
                    z['Event_Msg_Type'] == definitions.SUBSTITUTE_EVENT_MSG_TYPE
                ]
                df_lineups = process_substitution(z, df_lineups)

    df_lineups = df_lineups[
        df_lineups['Start_Canonical_Game_Event_Num'].notnull()
    ]
    df_lineups = df_lineups[
        df_lineups['End_Canonical_Game_Event_Num'].notnull()
    ]

    return df_lineups


def process_substitution(df_sub, df_lineups):
    for i in range(0, len(df_sub)):
        x = df_sub.iloc[i]
        event_id = x['Canonical_Game_Event_Num']
        player_out = x['Person1']
        player_in = x['Person2']
        team_id = x['Team_id']
        game_id = x['Game_id']
        period = x['Period']

        previous_lineup = \
            get_previous_lineup(df_lineups, game_id, team_id, period, event_id)
        sub_column = get_player_to_sub(previous_lineup, player_out)
        new_lineup = previous_lineup.copy()
        new_lineup[sub_column] = player_in
        new_lineup['Start_Canonical_Game_Event_Num'] = event_id
        previous_lineup['End_Canonical_Game_Event_Num'] = event_id
        df_lineups = df_lineups.append(new_lineup)
        df_lineups = df_lineups.append(previous_lineup)

    return df_lineups


def get_player_to_sub(lineup, player_id):
    for i in range(1, 5+1):
        column_name = "Player" + str(i)
        if lineup[column_name] == player_id:
            return column_name


def get_previous_lineup(df_lineups, game_id, team_id, period, event_id):
    df_lineups = df_lineups.loc[df_lineups['Period'] == period]
    df_lineups = df_lineups.loc[df_lineups['Game_id'] == game_id]
    df_lineups = df_lineups.loc[df_lineups['Team_id'] == team_id]
    previous_event_id = df_lineups['Start_Canonical_Game_Event_Num'].max()
    if previous_event_id > event_id:
        raise Exception("Event ids out of sequence")

    df_lineups = df_lineups.loc[
        df_lineups['Start_Canonical_Game_Event_Num'] == previous_event_id
    ]

    return df_lineups.iloc[0]


def get_period_starting_lineups(df):
    df_lineups = pd.DataFrame()

    game_ids = df['Game_id'].unique()
    for game_id in game_ids:
        x = df.loc[df['Game_id'] == game_id]
        team_ids = x['Team_id'].unique()
        for team_id in team_ids:
            y = x.loc[x['Team_id'] == team_id]
            for period in range(1, 4 + 1):
                z = y.loc[y['Period'] == period]
                df_lineup_row = get_lineup_row(z)
                df_lineups = df_lineups.append(df_lineup_row)
    return df_lineups


def get_lineup_row(df_decomposed_lineup):
    df_composed_lineup = pd.DataFrame()
    if (len(df_decomposed_lineup) != 5):
        raise Exception("Lineup size = " + len(df_decomposed_lineup))
    row = df_decomposed_lineup.iloc[0]
    df_composed_lineup['Game_id'] = pd.Series(row['Game_id'])
    df_composed_lineup['Team_id'] = pd.Series(row['Team_id'])
    df_composed_lineup['Period'] = pd.Series(row['Period'])

    canonical_event_id =\
        get_canonical_event_id(df_composed_lineup['Game_id'][0],
                               df_composed_lineup['Period'][0])
    df_composed_lineup['Start_Canonical_Game_Event_Num'] \
        = pd.Series(canonical_event_id)
    counter = 1
    for rows, columns in df_decomposed_lineup.iterrows():
        player_id = columns['Person_id']
        df_composed_lineup['Player' + str(counter)] = player_id
        counter = counter + 1

    return df_composed_lineup


def get_canonical_event_id(game_id, period):
    df = read_from_csv(definitions.DATA_DIR + "/tables/Canonical_Events.csv")
    df = df.loc[df['Period'] == period]
    df = df.loc[df['Game_id'] == game_id]
    df = df.loc[
        df['Event_Msg_Type'] == definitions.PERIOD_START_EVENT_MSG_TYPE
    ]
    df = df.loc[
        df['Action_Type'] == definitions.PERIOD_START_ACTION_TYPE
    ]

    return df['Canonical_Game_Event_Num'].iloc[0]


if __name__ == "__main__":
    main()
