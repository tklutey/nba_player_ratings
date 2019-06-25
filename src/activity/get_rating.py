def get_rating(df):
    df['OR'] = df['Num_points_offense'] * 100 / df['Possessions_offense']
    df['DR'] = df['Num_points_defense'] * 100 / df['Possessions_defense']
    df = df[['Player', 'OR', 'DR']]
    return df

