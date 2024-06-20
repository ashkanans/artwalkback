from enum import Enum


class UpdateFrequency(Enum):
    EVERY_MINUTE = 'every_minute'
    EVERY_5_MINUTES = 'every_5_minutes'
    EVERY_15_MINUTES = 'every_15_minutes'
    EVERY_30_MINUTES = 'every_30_minutes'
    EVERY_HOUR = 'every_hour'
    EVERY_6_HOURS = 'every_6_hours'
    EVERY_12_HOURS = 'every_12_hours'
    EVERY_DAY = 'every_day'
    EVERY_2_DAYS = 'every_2_days'
    EVERY_WEEK = 'every_week'
    EVERY_MONTH = 'every_month'