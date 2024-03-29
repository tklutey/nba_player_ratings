import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))


DATA_DIR = ROOT_DIR + "/data"
RAW_DATA_DIR = DATA_DIR + "/raw"

PERIOD_START_EVENT_MSG_TYPE = 12
PERIOD_START_ACTION_TYPE = 0
END_OF_PERIOD_EVENT_MSG_TYPE = 13

SUBSTITUTE_EVENT_MSG_TYPE = 8

MADE_BASKET_EVENT_MSG_TYPE = 1
MISSED_BASKET_EVENT_MSG_TYPE = 2

REBOUND_EVENT_MSG_TYPE = 4

TURNOVER_EVENT_MSG_TYPE = 5

FT_EVENT_MSG_TYPE = 3
FT_1_OF_1_ACTION_TYPE = 10
FT_1_OF_2_ACTION_TYPE = 11
FT_2_OF_2_ACTION_TYPE = 12
FT_3_OF_3_ACTION_TYPE = 15
FT_TECHNICAL_ACTION_TYPE = 16
FT_CLEAR_PATH_ACTION_TYPE = 17
FT_FLAGRANT_2_OF_2_ACTION_TYPE = 19
FT_FLAGRANT_1_OF_1_ACTION_TYPE = 20
FT_TECHNICAL_2_OF_2_ACTION_TYPE = 22
FT_CLEAR_PATH_2_OF_2_ACTION_TYPE = 26
FT_FLAGRANT_3_OF_3_ACTION_TYPE = 29

FOUL_EVENT_MSG_TYPE = 6
