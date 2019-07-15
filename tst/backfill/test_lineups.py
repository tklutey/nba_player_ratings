import unittest
import mock as mock

import pandas as pd
from pandas.util.testing import assert_frame_equal

import definitions
from src.backfill.lineups import canonical_events
from src.backfill.lineups.lineups import get_period_starting_lineups, apply_event_changes


class LineupBackfillTests(unittest.TestCase):

    def test_get_period_starting_lineups(self):
        canonical_events.get_canonical_event_id = mock.Mock(return_value=5)
        df_input = pd.DataFrame({'Game_id': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                                 'Period': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                                            2, 2, 2, 2, 2, 2, 2, 2, 2, 2,
                                            3, 3, 3, 3, 3, 3, 3, 3, 3, 3,
                                            4, 4, 4, 4, 4, 4, 4, 4, 4, 4],
                                 'Team_id': [1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
                                             1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
                                             1, 1, 1, 1, 1, 2, 2, 2, 2, 2,
                                             1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
                                 'Person_id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                               1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                               1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                               1, 2, 3, 4, 5, 6, 7, 8, 9, 10]})

        df_expected = pd.DataFrame({'Game_id': [1, 1, 1, 1, 1, 1, 1, 1],
                                    'Period': [1, 2, 3, 4, 1, 2, 3, 4],
                                    'Team_id': [1, 1, 1, 1, 2, 2, 2, 2],
                                    'Player1': [1, 1, 1, 1, 6, 6, 6, 6],
                                    'Player2': [2, 2, 2, 2, 7, 7, 7, 7],
                                    'Player3': [3, 3, 3, 3, 8, 8, 8, 8],
                                    'Player4': [4, 4, 4, 4, 9, 9, 9, 9],
                                    'Player5': [5, 5, 5, 5, 10, 10, 10, 10]})

        df_output = get_period_starting_lineups(df_input).reset_index(drop=True)[['Game_id', 'Period', 'Team_id',
                                                                                  'Player1', 'Player2', 'Player3',
                                                                                  'Player4', 'Player5']]

        assert_frame_equal(df_output, df_expected)

    def test_apply_subs(self):
        df_lineups = pd.DataFrame({'Game_id': [1, 1, 1],
                                   'Period': [1, 2, 3],
                                   'Team_id': [1, 1, 1],
                                   'Player1': [1, 1, 1],
                                   'Player2': [2, 2, 2],
                                   'Player3': [3, 3, 3],
                                   'Player4': [4, 4, 4],
                                   'Player5': [5, 5, 5],
                                   'Start_Canonical_Game_Event_Num': [1, 5, 10]
                                   })
        df_canonical_events = pd.DataFrame({'Game_id': [1, 1, 1, 1, 1],
                                            'Team_id': [1, 1, 1, 1, 1],
                                            'Period': [1, 1, 2, 2, 3],
                                            'Event_Msg_Type': [definitions.SUBSTITUTE_EVENT_MSG_TYPE,
                                                               definitions.END_OF_PERIOD_EVENT_MSG_TYPE,
                                                               definitions.SUBSTITUTE_EVENT_MSG_TYPE,
                                                               definitions.END_OF_PERIOD_EVENT_MSG_TYPE,
                                                               definitions.END_OF_PERIOD_EVENT_MSG_TYPE],
                                            'Canonical_Game_Event_Num': [2, 4, 6, 9, 11],
                                            'Person1': [1, 0, 2, 0, 0],
                                            'Person2': [6, 0, 7, 0, 0]})

        df_output = apply_event_changes(df_lineups, df_canonical_events).reset_index(drop=True)
        df_output = df_output.astype('int64')
        df_expected = pd.DataFrame({'Game_id': [1, 1, 1, 1, 1],
                                    'Team_id': [1, 1, 1, 1, 1],
                                    'Period': [1, 1, 2, 2, 3],
                                    'Start_Canonical_Game_Event_Num': [1, 2, 5, 6, 10],
                                    'End_Canonical_Game_Event_Num': [2, 4, 6, 9, 11],
                                    'Player1': [1, 6, 1, 1, 1],
                                    'Player2': [2, 2, 2, 7, 2],
                                    'Player3': [3, 3, 3, 3, 3],
                                    'Player4': [4, 4, 4, 4, 4],
                                    'Player5': [5, 5, 5, 5, 5]
                                    })

        assert_frame_equal(df_output.sort_index(axis=1), df_expected.sort_index(axis=1))
