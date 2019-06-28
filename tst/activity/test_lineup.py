import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal

from src.activity.lineups import join_lineup_by_event_id


class LineupTests(unittest.TestCase):

    def test_join_lineup_by_event_id(self):
        df_lineup = pd.DataFrame({'Game_id': [1, 2, 3], 'Team_id': [4, 5, 6],
                                  'Start_Canonical_Game_Event_Num': [1, 5, 10],
                                  'End_Canonical_Game_Event_Num': [4, 9, 14],
                                  'Player1': [1, 2, 3], 'Player2': [4, 5, 6], 'Player3': [7, 8, 9],
                                  'Player4': [10, 11, 12], 'Player5': [13, 14, 15]})
        df_events = pd.DataFrame({'Game_id': [1, 2, 3], 'Team_id': [4, 5, 6], 'Canonical_Game_Event_Num': [2, 6, 11],
                                  'Event_Msg_Type': [1, 2, 3], 'Action_Type': [0, 0, 0], 'Num_points': [2, 2, 2]})
        df_expected = pd.DataFrame({'Game_id': [1, 2, 3], 'Team_id': [4, 5, 6],
                                    'Start_Canonical_Game_Event_Num': [1, 5, 10],
                                    'End_Canonical_Game_Event_Num': [4, 9, 14],
                                   'Player1': [1, 2, 3], 'Player2': [4, 5, 6], 'Player3': [7, 8, 9],
                                    'Player4': [10, 11, 12], 'Player5': [13, 14, 15],
                                    'Canonical_Game_Event_Num': [2, 6, 11],
                                    'Event_Msg_Type': [1, 2, 3], 'Action_Type': [0, 0, 0], 'Num_points': [2, 2, 2]})
        df_output = join_lineup_by_event_id(df_events, df_lineup)
        assert_frame_equal(df_expected.sort_index(axis=1), df_output.sort_index(axis=1))
