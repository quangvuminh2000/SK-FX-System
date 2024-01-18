"""
Data types of indicators
"""

from enum import Enum


class TimeFrame(Enum):
    H1 = "1 hour"
    H4 = "4 hours"
    M1 = "1 minute"
    M5 = "5 minutes"
    M15 = "15 minutes"
    M30 = "30 minutes"
    D1 = "1 day"
    W1 = "1 week"
    M_1 = "1 month"
