from __future__ import annotations

from datetime import date, datetime, time, timedelta

from .models import AttendanceMetrics, ShiftRule, ShiftType
from .time_utils import timedelta_to_hours, timedelta_to_minutes

DAY_RULE = ShiftRule(
    start_offset=timedelta(hours=8),
    regular_end_offset=timedelta(hours=17),
    overtime_start_offset=timedelta(hours=18),
)
NIGHT_RULE = ShiftRule(
    start_offset=timedelta(hours=20),
    regular_end_offset=timedelta(days=1, hours=5),
    overtime_start_offset=timedelta(days=1, hours=5),
)

BREAK_DURATION = timedelta(hours=1)
MAX_REGULAR_DURATION = timedelta(hours=8)


def infer_shift_type(shift_text: str | None) -> ShiftType | None:
    text = (shift_text or "").strip()
    if "夜班" in text or "20:00" in text:
        return ShiftType.NIGHT
    if "白班" in text:
        return ShiftType.DAY
    return None


def calculate_attendance(
    base_date: date,
    punch_moments: list[datetime],
    shift_type: ShiftType,
) -> AttendanceMetrics:
    if not punch_moments:
        return AttendanceMetrics(
            regular_hours=0.0,
            overtime_hours=0.0,
            late_minutes=0,
            early_leave_minutes=0,
            has_punch=False,
        )

    ordered = sorted(punch_moments)
    first_punch = ordered[0]
    last_punch = ordered[-1]

    rule = DAY_RULE if shift_type == ShiftType.DAY else NIGHT_RULE
    anchor = datetime.combine(base_date, time.min)

    shift_start = anchor + rule.start_offset
    regular_end = anchor + rule.regular_end_offset
    overtime_start = anchor + rule.overtime_start_offset

    regular_hours = _calculate_regular_hours(first_punch, last_punch, shift_start, regular_end)
    overtime_hours = _calculate_overtime_hours(last_punch, overtime_start)
    late_minutes = _calculate_late_minutes(first_punch, shift_start)
    early_leave_minutes = _calculate_early_leave_minutes(last_punch, regular_end)

    return AttendanceMetrics(
        regular_hours=round(regular_hours, 2),
        overtime_hours=round(overtime_hours, 2),
        late_minutes=late_minutes,
        early_leave_minutes=early_leave_minutes,
        has_punch=True,
    )


def _calculate_regular_hours(
    first_punch: datetime,
    last_punch: datetime,
    shift_start: datetime,
    regular_end: datetime,
) -> float:
    overlap_start = max(first_punch, shift_start)
    overlap_end = min(last_punch, regular_end)

    if overlap_end <= overlap_start:
        return 0.0

    regular_duration = overlap_end - overlap_start
    regular_duration -= BREAK_DURATION

    if regular_duration < timedelta(0):
        regular_duration = timedelta(0)

    if regular_duration > MAX_REGULAR_DURATION:
        regular_duration = MAX_REGULAR_DURATION

    return timedelta_to_hours(regular_duration)


def _calculate_overtime_hours(last_punch: datetime, overtime_start: datetime) -> float:
    if last_punch <= overtime_start:
        return 0.0
    return timedelta_to_hours(last_punch - overtime_start)


def _calculate_late_minutes(first_punch: datetime, shift_start: datetime) -> int:
    if first_punch <= shift_start:
        return 0
    return timedelta_to_minutes(first_punch - shift_start)


def _calculate_early_leave_minutes(last_punch: datetime, regular_end: datetime) -> int:
    if last_punch >= regular_end:
        return 0
    return timedelta_to_minutes(regular_end - last_punch)
