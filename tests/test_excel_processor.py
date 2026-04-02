from __future__ import annotations

from datetime import datetime, time

from attendance_tool.excel_processor import _infer_shift_from_punch_values
from attendance_tool.models import ShiftType


def test_infer_shift_from_punch_values_returns_day_for_morning_start() -> None:
    shift = _infer_shift_from_punch_values(["07:50", "17:05"])
    assert shift == ShiftType.DAY


def test_infer_shift_from_punch_values_returns_night_for_next_day_hint() -> None:
    shift = _infer_shift_from_punch_values(["20:05", "次日05:10"])
    assert shift == ShiftType.NIGHT


def test_infer_shift_from_punch_values_returns_night_for_early_morning_time() -> None:
    shift = _infer_shift_from_punch_values([time(20, 2), datetime(2026, 3, 25, 4, 50)])
    assert shift == ShiftType.NIGHT
