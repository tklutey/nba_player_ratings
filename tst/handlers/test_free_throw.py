import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal

from definitions import FOUL_EVENT_MSG_TYPE, FT_2_OF_2_ACTION_TYPE, FT_EVENT_MSG_TYPE, FT_1_OF_2_ACTION_TYPE
from src.handlers import free_throw


class FTTests(unittest.TestCase):

    def test_filter_and_generate_columns(self):
        df_canonical = pd.DataFrame({'Canonical_Game_Event_Num': [1, 2, 3], 'Game_id': [1, 1, 1],
                                 'Event_Msg_Type': [FOUL_EVENT_MSG_TYPE, FT_EVENT_MSG_TYPE, FT_EVENT_MSG_TYPE],
                                     'Action_Type': [0, FT_1_OF_2_ACTION_TYPE, FT_2_OF_2_ACTION_TYPE],
                                     'Attempted_points': [0, 1, 1]})

        df_filter = free_throw.filter(df_canonical)

        df_output = free_throw.generate_columns(df_filter, df_canonical)[['Canonical_Game_Event_Num', 'Game_id', 'Event_Msg_Type', 'Action_Type', 'Actualized_points', 'Actualized_Canonical_Game_Event_Num']].reset_index(drop=True)
        df_expected = pd.DataFrame(
            {'Canonical_Game_Event_Num': [3], 'Game_id': [1],
             'Event_Msg_Type': [FT_EVENT_MSG_TYPE], 'Action_Type': [FT_2_OF_2_ACTION_TYPE], 'Actualized_points': [2], 'Actualized_Canonical_Game_Event_Num': [1]})

        assert_frame_equal(df_output, df_expected)
