import pandas as pd

from definitions import MISSED_BASKET_EVENT_MSG_TYPE, REBOUND_EVENT_MSG_TYPE


def handle(df):
    df = filter(df)
    df = get_actualized_points(df)
    df = get_actualized_event_id(df)
    return df


def filter(df):
    df_next = df.copy()
    df = df.loc[df['Event_Msg_Type'] == MISSED_BASKET_EVENT_MSG_TYPE].copy()
    df['Next_event_id'] = df['Canonical_Game_Event_Num'] + 1
    df = pd.merge(left=df, right=df_next, how='inner',
                  left_on=['Game_id', 'Next_event_id'],
                  right_on=['Game_id', 'Canonical_Game_Event_Num'],
                  suffixes=('', '_y'))
    df = df.loc[df['Event_Msg_Type_y'] == REBOUND_EVENT_MSG_TYPE]
    return df


def get_actualized_points(df):
    df['Actualized_points'] = 0
    return df


def get_actualized_event_id(df):
    df['Actualized_Canonical_Game_Event_Num'] = df['Canonical_Game_Event_Num']
    return df
