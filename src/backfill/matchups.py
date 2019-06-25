import pandas as pd

from definitions import RAW_DATA_DIR, DATA_DIR
from src.backfill.lineups import GAME_LINEUP_DATA
from src.util.csv_persistence import read_from_csv, write_to_csv


def main():
    df = read_from_csv(RAW_DATA_DIR + GAME_LINEUP_DATA)
    game_ids = df['Game_id'].unique()

    games = pd.DataFrame()

    for game_id in game_ids:
        y = df.loc[df['Game_id'] == game_id]

        team_ids = y['Team_id'].unique()
        if len(team_ids) != 2:
            raise Exception("Multiple teams in game!")
        a = pd.DataFrame()
        a['Game_id'] = pd.Series(game_id)
        counter = 1

        for team_id in team_ids:
            key = 'Team' + str(counter)
            print(key)
            a[key] = pd.Series(team_id)
            counter = counter + 1
        games = games.append(a)
    write_to_csv(games, DATA_DIR + "/tables/Matchups.csv")



if __name__ == "__main__":
    print(main())