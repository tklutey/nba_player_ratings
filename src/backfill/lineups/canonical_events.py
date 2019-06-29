import definitions
from src.util.csv_persistence import read_from_csv


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
