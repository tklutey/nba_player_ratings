from definitions import FT_EVENT_MSG_TYPE, FT_1_OF_1_ACTION_TYPE, FT_2_OF_2_ACTION_TYPE, FT_3_OF_3_ACTION_TYPE, \
    FT_TECHNICAL_ACTION_TYPE, FT_CLEAR_PATH_ACTION_TYPE, FT_FLAGRANT_2_OF_2_ACTION_TYPE, FT_FLAGRANT_1_OF_1_ACTION_TYPE, \
    FT_TECHNICAL_2_OF_2_ACTION_TYPE, FT_CLEAR_PATH_2_OF_2_ACTION_TYPE, FT_FLAGRANT_3_OF_3_ACTION_TYPE, \
    FOUL_EVENT_MSG_TYPE


def handle(df):
    df_filtered = filter(df)
    df = generate_columns(df_filtered, df)
    return df

def filter(df):
    df = get_last_ft_events(df)
    return df

def generate_columns(df_filtered, df_canonical):
    print('Logging foul events. This might take a second...')
    for index, row in df_filtered.iterrows():
        values = back_iterate_ft(row, df_canonical)
        points = values['Actualized_points']
        source_event_id = values['Foul_event_id']
        df_filtered['Actualized_points'] = points
        df_filtered['Actualized_Canonical_Game_Event_Num'] = source_event_id
    return df_filtered

def back_iterate_ft(row, df_canonical):
    points = 0
    points = points + get_row_attempted_points(row)
    cur_row = get_prev_row(row, df_canonical)
    while cur_row['Event_Msg_Type'] != FOUL_EVENT_MSG_TYPE:
        if cur_row['Event_Msg_Type'] == FT_EVENT_MSG_TYPE:
            points = points + get_row_attempted_points(cur_row)
        cur_row = get_prev_row(cur_row, df_canonical)
    foul_event_id = cur_row['Canonical_Game_Event_Num']
    return {
        "Foul_event_id": foul_event_id,
        "Actualized_points": points
    }


def get_row_attempted_points(row):
    return row['Attempted_points']

def get_prev_row(row, df):
    return df.loc[(df['Game_id'] == row['Game_id'])
                                & (df['Canonical_Game_Event_Num'] == row['Canonical_Game_Event_Num'] - 1)].iloc[0].copy()

def get_last_ft_events(df):
    df = df.loc[df['Event_Msg_Type'] == FT_EVENT_MSG_TYPE].copy()
    df = df.loc[(df['Action_Type'] == FT_1_OF_1_ACTION_TYPE)
                | (df['Action_Type'] == FT_2_OF_2_ACTION_TYPE)
                | (df['Action_Type'] == FT_3_OF_3_ACTION_TYPE)
                | (df['Action_Type'] == FT_TECHNICAL_ACTION_TYPE)
                | (df['Action_Type'] == FT_CLEAR_PATH_ACTION_TYPE)
                | (df['Action_Type'] == FT_FLAGRANT_2_OF_2_ACTION_TYPE)
                | (df['Action_Type'] == FT_FLAGRANT_1_OF_1_ACTION_TYPE)
                | (df['Action_Type'] == FT_TECHNICAL_2_OF_2_ACTION_TYPE)
                | (df['Action_Type'] == FT_CLEAR_PATH_2_OF_2_ACTION_TYPE)
                | (df['Action_Type'] == FT_FLAGRANT_3_OF_3_ACTION_TYPE)
    ].copy()

    return df