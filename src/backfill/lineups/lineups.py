import pandas as pd

import definitions
from src.backfill.lineups import canonical_events
from src.util.csv_persistence import read_from_csv, write_to_csv

GAME_LINEUP_DATA = "/csv/Game_Lineup.csv"


def main():
    df_lineups = read_from_csv(definitions.RAW_DATA_DIR + GAME_LINEUP_DATA)
    df_canonical = read_from_csv(definitions.DATA_DIR + "/tables/Canonical_Events.csv")

    df_lineups = get_period_starting_lineups(df_lineups)
    df_lineups = apply_event_changes(df_lineups, df_canonical)
    write_to_csv(df_lineups, definitions.DATA_DIR + "/tables/Lineups.csv")


def apply_event_changes(df_lineups, df_canonical):
    print("Applying event changes...")
    df = df_canonical.groupby(['Game_id', 'Team_id'], as_index=False).apply(lambda x: get_period_events(x, df_lineups))
    df = df[
        df['Start_Canonical_Game_Event_Num'].notnull()
    ]
    df = df[
        df['End_Canonical_Game_Event_Num'].notnull()
    ]
    return df


def get_period_events(df_canonical, df_lineups):
    df = df_canonical.loc[df_canonical['Period'] != 0]
    df = df.groupby('Period', as_index=False).apply(lambda x: filter_process_events(x, df_lineups))
    df = df.reset_index(drop=True)
    return df


def filter_process_events(df_canonical, df_lineups):
    z = df_canonical.loc[
        (df_canonical['Event_Msg_Type'] == definitions.SUBSTITUTE_EVENT_MSG_TYPE)
        | (df_canonical['Event_Msg_Type'] == definitions.END_OF_PERIOD_EVENT_MSG_TYPE)
    ]
    if len(z) > 0:
        s = process_event(z, df_lineups)
        return s
    return None


def process_event(df_sub, df_lineups):
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

        if x['Event_Msg_Type'] == definitions.SUBSTITUTE_EVENT_MSG_TYPE:
            new_lineup = previous_lineup.copy()

            sub_column = get_player_to_sub(previous_lineup, player_out)
            new_lineup[sub_column] = player_in
            new_lineup['Start_Canonical_Game_Event_Num'] = event_id
            df_lineups = df_lineups.append(new_lineup, sort=True)

        previous_lineup['End_Canonical_Game_Event_Num'] = event_id
        df_lineups = df_lineups.append(previous_lineup, sort=True)

    return df_lineups


def get_player_to_sub(lineup, player_id):
    for i in range(1, 5+1):
        column_name = "Player" + str(i)
        if lineup[column_name].iloc[0] == player_id:
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

    return df_lineups


def get_period_starting_lineups(df):
    print("Creating period starting lineups...")
    return df.groupby(['Game_id', 'Team_id']).apply(get_period_lineups)


def get_period_lineups(df):
    df = df.loc[df['Period'] != 0]
    return df.groupby('Period').apply(get_lineup_row)


def get_lineup_row(df_decomposed_lineup):
    df_composed_lineup = pd.DataFrame()
    if len(df_decomposed_lineup) != 5 & len(df_decomposed_lineup) != 0:
        raise Exception("Lineup size = " + str(len(df_decomposed_lineup)))
    row = df_decomposed_lineup.iloc[0]
    df_composed_lineup['Game_id'] = pd.Series(row['Game_id'])
    df_composed_lineup['Team_id'] = pd.Series(row['Team_id'])
    df_composed_lineup['Period'] = pd.Series(row['Period'])

    canonical_event_id =\
        canonical_events.get_canonical_event_id(df_composed_lineup['Game_id'][0],
                                                df_composed_lineup['Period'][0])
    df_composed_lineup['Start_Canonical_Game_Event_Num'] \
        = pd.Series(canonical_event_id)
    counter = 1
    for rows, columns in df_decomposed_lineup.iterrows():
        player_id = columns['Person_id']
        df_composed_lineup['Player' + str(counter)] = player_id
        counter = counter + 1
    return df_composed_lineup


if __name__ == "__main__":
    main()
