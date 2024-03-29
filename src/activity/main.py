from definitions import DATA_DIR
from src.activity import get_rating
from src.converter import player_totals
from src.handlers import made_fg, missed_fg, turnover, end_period, free_throw
from src.util import csv_persistence


def process_events():
    df = csv_persistence.read_from_csv(DATA_DIR + "/tables/Canonical_Events.csv")
    x = append_actualized_values(df)
    y = player_totals.get_player_points(x)
    z = get_rating.get_rating(y).reset_index(drop=True)
    csv_persistence.write_to_csv(z, DATA_DIR + "/output/Ratings.csv")
    print(z)


def append_actualized_values(df):
    # Made FG
    a = made_fg.handle(df)
    # Missed FG followed by def rebound
    b = missed_fg.handle(df)
    # Turnover
    c = turnover.handle(df)
    # End of period
    d = end_period.handle(df)
    # FT
    e = free_throw.handle(df)

    result = a.append(b, sort=True).append(c, sort=True).append(d, sort=True).append(e, sort=True)

    return result


if __name__ == "__main__":
    process_events()
