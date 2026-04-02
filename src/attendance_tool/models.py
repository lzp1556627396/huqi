from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from enum import Enum


class ShiftType(str, Enum):
    DAY = "day"
    NIGHT = "night"


@dataclass(frozen=True)
class ShiftRule:
    start_offset: timedelta
    regular_end_offset: timedelta
    overtime_start_offset: timedelta


@dataclass(frozen=True)
class AttendanceMetrics:
    regular_hours: float
    overtime_hours: float
    late_minutes: int
    early_leave_minutes: int
    has_punch: bool

