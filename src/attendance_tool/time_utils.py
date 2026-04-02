from __future__ import annotations

import re
from datetime import date, datetime, time, timedelta
from typing import Any

from .models import ShiftType

INVALID_PUNCH_VALUES = {"", "--", "未打卡", "nan", "none", "nat", "null"}
DATE_PATTERN = re.compile(r"(\d{4})[/-](\d{1,2})[/-](\d{1,2})")
TIME_PATTERN = re.compile(r"^(次日)?\s*(\d{1,2}):(\d{2})$")


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def parse_work_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value

    text = normalize_text(value)
    if not text:
        return None

    matched = DATE_PATTERN.search(text)
    if not matched:
        return None

    year, month, day = (int(part) for part in matched.groups())
    return date(year, month, day)


def parse_punch_datetime(value: Any, base_date: date, shift_type: ShiftType) -> datetime | None:
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, time):
        moment = datetime.combine(base_date, value)
        if shift_type == ShiftType.NIGHT and value.hour < 12:
            moment += timedelta(days=1)
        return moment

    text = normalize_text(value)
    if not text:
        return None
    if text.lower() in INVALID_PUNCH_VALUES:
        return None

    matched = TIME_PATTERN.match(text)
    if not matched:
        return None

    is_next_day, hour_text, minute_text = matched.groups()
    hour = int(hour_text)
    minute = int(minute_text)

    moment = datetime.combine(base_date, time(hour=hour, minute=minute))

    if is_next_day:
        moment += timedelta(days=1)
    elif shift_type == ShiftType.NIGHT and hour < 12:
        moment += timedelta(days=1)

    return moment


def timedelta_to_hours(value: timedelta) -> float:
    return value.total_seconds() / 3600


def timedelta_to_minutes(value: timedelta) -> int:
    return int(value.total_seconds() // 60)


def format_late_early_text(late_minutes: int, early_leave_minutes: int, has_punch: bool) -> str:
    if not has_punch:
        return "无打卡记录"
    if late_minutes <= 0 and early_leave_minutes <= 0:
        return "无"
    if late_minutes > 0 and early_leave_minutes > 0:
        return f"迟到{late_minutes}分钟；早退{early_leave_minutes}分钟"
    if late_minutes > 0:
        return f"迟到{late_minutes}分钟"
    return f"早退{early_leave_minutes}分钟"
