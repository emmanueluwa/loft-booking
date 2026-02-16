from datetime import time, datetime
from enum import Enum


class Weekday(int, Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


WORKING_HOURS = {
    Weekday.MONDAY: (time(14, 30), time(18, 0)),
    Weekday.WEDNESDAY: (time(9, 0), time(17, 0)),
    Weekday.THURSDAY: (time(9, 0), time(17, 0)),
    Weekday.SATURDAY: (time(10, 0), time(16, 0)),
}


def is_working_day(date: datetime) -> bool:
    return date.weekday() in WORKING_HOURS


def get_working_hours(date: datetime) -> tuple[time, time] | None:
    return WORKING_HOURS.get(date.weekday())
