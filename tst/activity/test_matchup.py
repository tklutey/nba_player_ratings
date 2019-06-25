import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal

from src.activity.matchups import get_matchup_by_game_ids


class MatchupTests(unittest.TestCase):

    def test_get_matchup_by_game_ids(self):
        df_input = pd.DataFrame({'Game_id': [1, 2], 'Team_id': [3, 6]})
        df_matchups = pd.DataFrame({'Game_id': [1, 2], 'Team1': [3, 4], 'Team2': [5, 6]})
        df_output = get_matchup_by_game_ids(df_input, df_matchups)
        df_expected = pd.DataFrame({'Game_id': [1, 2], 'Off_team': [3, 6], 'Def_team': [5, 4]})
        assert_frame_equal(df_output, df_expected)
