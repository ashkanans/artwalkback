from datetime import datetime

persian_to_english_digit_map = {
    '۰': '0',
    '۱': '1',
    '۲': '2',
    '۳': '3',
    '۴': '4',
    '۵': '5',
    '۶': '6',
    '۷': '7',
    '۸': '8',
    '۹': '9'
}

index_abbr = {
    'Dollar': 'usd',
    'AED': 'aed',
    'Eur': 'eur',
    'Gbp': 'gbp',
    'OnsG': 'nnsg',
    'Seke': 'seke',
}


def extractDateTime(date, day):
    day_str = str(day).zfill(8)
    time_str = str(date).zfill(6)
    datetime_str = time_str + "_" + day_str
    formatted_datetime = datetime.strptime(datetime_str, "%H%M%S_%Y%m%d")
    return formatted_datetime.strftime("%Y-%m-%d_%H-%M-%S")
