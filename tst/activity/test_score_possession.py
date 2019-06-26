import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal

from src.activity.score_possession import process


class ScorePossessionTests(unittest.TestCase):

    def test_process(self):
        suffix = 'offense'
        df = pd.DataFrame({'Player1': [1, 2, 3], 'Player2': [1, 2, 3], 'Player3': [1, 2, 3], 'Player4': [4, 5, 6],
                           'Player5': [4, 5, 6], 'Actualized_points': [2, 2, 2]})
        df_process = process(df, suffix)
        df_expected = pd.DataFrame({'Player': [1, 2, 3, 4, 5, 6], 'Actualized_points_' + suffix: [6, 6, 6, 4, 4, 4], 'Possessions_' + suffix: [3, 3, 3, 2, 2, 2]})
        assert_frame_equal(df_process, df_expected)