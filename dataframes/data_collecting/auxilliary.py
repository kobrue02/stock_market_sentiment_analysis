import datetime
import time
from datetime import date, timedelta


def tweet_to_dmy(date: str):
    """
    extracts the date from a tweet object and returns it in D-M-Y format
    """
    toks = str(date.split(" ")[0]).split("-")
    month = toks[1]
    day = toks[2]
    year = toks[0]
    return f"{day}-{month}-{year}"


def unix_timestamp(date):
    """
    helper method to convert a date from D-M-Y format to unix timestamp using datetime and time
    data param has to be in string format. e.g. "01-12-2022"
    """
    chops = date.split("-")
    date = datetime.date(int(chops[2]), int(chops[1]), int(chops[0]))
    return str(int(time.mktime(date.timetuple())))


def twit_format(date):
    """
    helper method that converts date from D-M-Y format to Y-M-D and adds T00:00:00Z
    """
    chops = date.split("-")
    year = chops[2]
    month = chops[1]
    day = chops[0]
    new_date = f"{year}-{month}-{day}T00:00:00Z"
    return new_date


def vantage_date(date):
    """
    turns date from D-M-Y format to Y-M-D which is required by alpha vantage api
    """
    start_chops = date.split("-")
    month = int(start_chops[1])  # the input is a string like "12-05-2022"
    year = int(start_chops[2])  # so the first slice is the day and so on
    day = int(start_chops[0])
    if day < 10:
        day = f"0{day}"
    return f"{year}-{month}-{day}"


def calc_day_after(sdate):
    """
    simple method to increase the day in a D-M-Y date string by 1
    """
    current_date = string_to_date(sdate)
    next_day = current_date + timedelta(days=1)
    return next_day.strftime("%d-%m-%Y")


def calc_day_before(sdate):
    """
    simple method to decrease the day in a D-M-Y date string by 1
    """
    current_date = string_to_date(sdate)
    previous_day = current_date - timedelta(days=1)
    return previous_day.strftime("%d-%m-%Y")


def string_to_date(strdate):
    """
    turns a date in string format using D-M-Y to a date object
    """
    chops = strdate.split("-")
    month = int(chops[1])  # the input is a string like "12-05-2022"
    year = int(chops[2])  # so the first slice is the day and so on
    day = int(chops[0])
    sdate = date(year, month, day)  # datetime date object so pandas can work w it
    return sdate
