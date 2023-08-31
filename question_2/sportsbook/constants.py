"""
This python file is used to declare all the constants used across the project
"""

from enum import StrEnum

class Tables(StrEnum):
    """
    This enum maintains list of tables available in the database
    """
    SPORTS = 'sports'
    EVENTS = 'events'
    SELECTIONS = 'selections'

VALID_EVENT_TYPE = ['preplay', 'inplay']
VALID_EVENT_STATUS = ['pending', 'started', 'ended', 'cancelled']
VALID_SELECTION_OUTCOME = ['unsettled', 'void', 'lose', 'win']
VALID_CONDITIONS = ['=', '>', '<', '>=', '<=','like', 'between']