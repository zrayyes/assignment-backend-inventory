import datetime
from datetime import date


def date_after_n_days(days: int) -> date:
    return datetime.date.today() + datetime.timedelta(days=days)


def format_date_to_str(date: date) -> str:
    return date.strftime("%d/%m/%Y")


def format_str_to_date(date_str: str) -> date:
    return datetime.datetime.strptime(date_str, "%d/%m/%Y").date()
