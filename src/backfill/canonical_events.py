import pandas as pd
from definitions import RAW_DATA_DIR, DATA_DIR

def main():
    df = read_from_csv()
    df = create_canonical_event_number(df)
    write_to_csv(df)

def create_canonical_event_number(dataframe):
    game_ids = dataframe['Game_id'].unique()
    df = pd.DataFrame()

    for id in game_ids:
        x = dataframe.loc[dataframe['Game_id'] == id]
        df_sorted = x.sort_values(by=['Period', 'PC_Time', 'WC_Time', 'Event_Num'],
                                   ascending=[True, False, True, True])

        df_sorted = df_sorted.reset_index(drop=True)
        df_sorted['Canonical_Game_Event_Num'] = df_sorted.index

        df_sorted = df_sorted.drop('Event_Num', axis=1)

        df = df.append(df_sorted)
    df = df.reset_index(drop=True)
    return df

def read_from_csv():
    return pd.read_csv(RAW_DATA_DIR + "/csv/Play_by_play.csv", index_col=False)

def write_to_csv(df):
    df.to_csv(DATA_DIR + "/tables/Canonical_Events.csv")

if __name__ == "__main__":
    main()