import datetime
from datetime import date


def date_after_n_days(days: int) -> date:
    return datetime.date.today() + datetime.timedelta(days=days)


def format_date_to_str(date: date) -> str:
    return date.strftime("%d/%m/%Y, %H:%M:%S")
