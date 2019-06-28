import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal

from src.activity.score_possession import process


class ScorePossessionTests(unittest.TestCase):

    def test_process(self):
        suffix = 'offense'
        df = pd.DataFrame({'Game_id': [1, 1, 2], 'Player1': [1, 1, 1], 'Player2': [2, 2, 2], 'Player3': [3, 3, 3], 'Player4': [4, 4, 4],
                           'Player5': [5, 5, 5], 'Actualized_points': [2, 2, 2]})
        df_process = process(df, suffix)[['Player', 'Game_id', 'Actualized_points_' + suffix, 'Possessions_' + suffix]]
        df_expected = pd.DataFrame({'Player': [1, 1, 2, 2, 3, 3, 4, 4, 5, 5], 'Game_id': [1, 2, 1, 2, 1, 2, 1, 2, 1, 2], 'Actualized_points_' + suffix: [4, 2, 4, 2, 4, 2, 4, 2, 4, 2], 'Possessions_' + suffix: [2, 1, 2, 1, 2, 1, 2, 1, 2, 1]})
        assert_frame_equal(df_process, df_expected)