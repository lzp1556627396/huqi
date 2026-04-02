from __future__ import annotations

from datetime import date, datetime, time

from attendance_tool.models import ShiftType
from attendance_tool.time_utils import parse_punch_datetime


def test_parse_time_for_day_shift_stays_same_day() -> None:
    base = date(2026, 3, 24)
    parsed = parse_punch_datetime(time(7, 50), base, ShiftType.DAY)
    assert parsed == datetime(2026, 3, 24, 7, 50)


def test_parse_time_for_night_shift_before_noon_becomes_next_day() -> None:
    base = date(2026, 3, 24)
    parsed = parse_punch_datetime(time(2, 15), base, ShiftType.NIGHT)
    assert parsed == datetime(2026, 3, 25, 2, 15)
