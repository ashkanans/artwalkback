from jdatetime import datetime as jdtime


def gregorian_to_shamsi(gregorian_date):
    gregorian_date_parts = gregorian_date.split('-')
    year = int(gregorian_date_parts[0])
    month = int(gregorian_date_parts[1])
    day = int(gregorian_date_parts[2])

    # Convert to Persian (Shamsi) date
    shamsi_date = jdtime.fromgregorian(year=year, month=month, day=day).strftime('%Y/%m/%d')

    return shamsi_date
