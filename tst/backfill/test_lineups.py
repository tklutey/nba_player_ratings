import unittest
import mock as mock

import pandas as pd
from pandas.util.testing import assert_frame_equal

from src.backfill.lineups import canonical_events
from src.backfill.lineups.lineups import get_period_starting_lineups


class LineupBackfillTests(unittest.TestCase):

    def test_get_period_starting_lineups(self):
        canonical_events.get_canonical_event_id = mock.Mock(return_value=5)
        df_input = pd.DataFrame({'Game_id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 'Period': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
                                            3, 3, 3, 3, 3, 4, 4, 4, 4, 4],
                                 'Team_id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                             1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 'Person_id': [1, 2, 3, 4, 5, 1, 2, 3, 4, 5,
                                               1, 2, 3, 4, 5, 1, 2, 3, 4, 5]})

        df_expected = pd.DataFrame({'Game_id': [1, 1, 1, 1],
                                    'Period': [1, 2, 3, 4],
                                    'Team_id': [1, 1, 1, 1],
                                    'Player1': [1, 1, 1, 1],
                                    'Player2': [2, 2, 2, 2],
                                    'Player3': [3, 3, 3, 3],
                                    'Player4': [4, 4, 4, 4],
                                    'Player5': [5, 5, 5, 5]})

        df_output = get_period_starting_lineups(df_input).reset_index(drop=True)[['Game_id', 'Period', 'Team_id',
                                                                                  'Player1', 'Player2', 'Player3',
                                                                                  'Player4', 'Player5']]

        assert_frame_equal(df_output, df_expected)
