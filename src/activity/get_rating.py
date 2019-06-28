def get_rating(df):
    df['OR'] = df['Actualized_points_offense'] * 100 / df['Possessions_offense']
    df['DR'] = df['Actualized_points_defense'] * 100 / df['Possessions_defense']
    df = df[['Player', 'OR', 'DR']]
    return df

