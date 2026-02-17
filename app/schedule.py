from datetime import time, datetime, timedelta
from enum import Enum
from zoneinfo import ZoneInfo

from app.services import SERVICE_DURATIONS, ServiceType

LONDON_TZ = ZoneInfo("Europe/London")


class Weekday(int, Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


WORKING_HOURS: dict[Weekday, tuple[time, time]] = {
    Weekday.MONDAY: (time(14, 30), time(18, 0)),
    Weekday.WEDNESDAY: (time(9, 0), time(17, 0)),
    Weekday.THURSDAY: (time(9, 0), time(17, 0)),
    Weekday.SATURDAY: (time(10, 0), time(16, 0)),
}


def get_available_slots(
    date: datetime, service: ServiceType, booked_slots: list[tuple[datetime, datetime]]
) -> list[datetime]:
    weekday = Weekday(date.weekday())

    if weekday not in WORKING_HOURS:
        return []

    start_time, end_time = WORKING_HOURS[weekday]
    service_duration = SERVICE_DURATIONS[service]

    slots = []
    slot_start_time = datetime(
        date.year,
        date.month,
        date.day,
        start_time.hour,
        start_time.minute,
        tzinfo=LONDON_TZ,
    )

    end = datetime(
        date.year,
        date.month,
        date.day,
        end_time.hour,
        end_time.minute,
        tzinfo=LONDON_TZ,
    )

    while slot_start_time + service_duration <= end:
        slot_end = slot_start_time + service_duration

        is_available = not any(
            slot_start_time < booking_end and slot_end > booking_start
            for booking_start, booking_end in booked_slots
        )

        if is_available:
            slots.append(slot_start_time)

        slot_start_time += timedelta(minutes=15)

    return slots
