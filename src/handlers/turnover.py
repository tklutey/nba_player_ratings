from definitions import TURNOVER_EVENT_MSG_TYPE


def handle(df):
    df = filter(df)
    df = get_actualized_points(df)
    df = get_actualized_event_id(df)
    return df

def filter(df):
    return df.loc[df['Event_Msg_Type'] == TURNOVER_EVENT_MSG_TYPE].copy()

def get_actualized_points(df):
    df['Actualized_points'] = 0
    return df

def get_actualized_event_id(df):
    df['Actualized_Canonical_Game_Event_Num'] = df['Canonical_Game_Event_Num']
    return df