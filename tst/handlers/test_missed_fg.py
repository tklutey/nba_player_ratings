import unittest

import pandas as pd
from pandas.util.testing import assert_frame_equal

from definitions import MISSED_BASKET_EVENT_MSG_TYPE, REBOUND_EVENT_MSG_TYPE
from src.handlers import missed_fg


class MissedFGTests(unittest.TestCase):

    def test_filter(self):
        df_input = pd.DataFrame({'Canonical_Game_Event_Num': [1, 2, 1, 2], 'Game_id': [1, 1, 2, 2],
                                 'Event_Msg_Type': [MISSED_BASKET_EVENT_MSG_TYPE, 0, MISSED_BASKET_EVENT_MSG_TYPE, REBOUND_EVENT_MSG_TYPE]})

        df_output = missed_fg.filter(df_input)[['Canonical_Game_Event_Num', 'Game_id', 'Event_Msg_Type']].reset_index(drop=True)
        df_expected = pd.DataFrame(
            {'Canonical_Game_Event_Num': [1], 'Game_id': [2],
             'Event_Msg_Type': [MISSED_BASKET_EVENT_MSG_TYPE]})

        assert_frame_equal(df_output, df_expected)
