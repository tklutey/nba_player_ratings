def get_rating(df):
    df['OffRtg'] = df['Actualized_points_offense'] * 100 / df['Possessions_offense']
    df['DefRtg'] = df['Actualized_points_defense'] * 100 / df['Possessions_defense']
    df = df[['Player', 'Game_id', 'OffRtg', 'DefRtg']]
    df = df.rename(columns={"Player": "Player_ID", "Game_ID": "Game_id"})
    return df

