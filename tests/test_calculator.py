from __future__ import annotations

from datetime import date, datetime

from attendance_tool.calculator import calculate_attendance, infer_shift_type
from attendance_tool.models import ShiftType


def test_day_shift_full_regular_no_overtime() -> None:
    base = date(2026, 3, 24)
    punches = [
        datetime(2026, 3, 24, 7, 50),
        datetime(2026, 3, 24, 17, 5),
    ]
    result = calculate_attendance(base, punches, ShiftType.DAY)
    assert result.regular_hours == 8.0
    assert result.overtime_hours == 0.0
    assert result.late_minutes == 0
    assert result.early_leave_minutes == 0
    assert result.has_punch is True


def test_day_shift_late_and_early_leave() -> None:
    base = date(2026, 3, 24)
    punches = [
        datetime(2026, 3, 24, 8, 20),
        datetime(2026, 3, 24, 16, 40),
    ]
    result = calculate_attendance(base, punches, ShiftType.DAY)
    assert result.regular_hours == 7.33
    assert result.overtime_hours == 0.0
    assert result.late_minutes == 20
    assert result.early_leave_minutes == 20


def test_night_shift_regular_and_overtime() -> None:
    base = date(2026, 3, 23)
    punches = [
        datetime(2026, 3, 23, 19, 53),
        datetime(2026, 3, 24, 8, 1),
    ]
    result = calculate_attendance(base, punches, ShiftType.NIGHT)
    assert result.regular_hours == 8.0
    assert result.overtime_hours == 3.02
    assert result.late_minutes == 0
    assert result.early_leave_minutes == 0


def test_no_punch_record_returns_zero() -> None:
    base = date(2026, 3, 24)
    result = calculate_attendance(base, [], ShiftType.DAY)
    assert result.regular_hours == 0.0
    assert result.overtime_hours == 0.0
    assert result.late_minutes == 0
    assert result.early_leave_minutes == 0
    assert result.has_punch is False


def test_infer_shift_type() -> None:
    assert infer_shift_type("白班A：08:00-12:00、13:00-17:00") == ShiftType.DAY
    assert infer_shift_type("夜班：20:00-24:00、次日01:00-次日05:00") == ShiftType.NIGHT
    assert infer_shift_type("--") is None
