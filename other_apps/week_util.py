from datetime import datetime,timedelta


def getWeekDate(): 
    date=datetime.today() 
    newdate=date 
    start_of_week = newdate - timedelta(days = newdate.weekday()) 
    start_of_week=start_of_week-timedelta(days=1)
    end_of_week = start_of_week + timedelta(days = 7)    
    return [start_of_week,end_of_week]
    # return [(start_of_week+timedelta(days=x)) for x in range(7)]

 
# for day"%aA"
def getMonthRange(year, month):
    """Return the last date of the month.
    
    Args:
        year (int): Year, i.e. 2022
        month (int): Month, i.e. 1 for January

    Returns:
        date (datetime): Last date of the current month
    """
    now=datetime.now()
    if month == 12:
        last_date = datetime(year, month, 31)
    else:
        last_date = datetime(year, month + 1, 1) + timedelta(days=-1)
    start_date=datetime(year, month, 1)
    return [start_date.date(),last_date.date() ]


now=datetime.now()
# print(getMonthRange(now.year,now.month+2))
import calendar
def get_no_of_week():
    return len(calendar.monthcalendar(2019, 3))

from datetime import datetime, timedelta
def get_week_dates():

    day = '12/Oct/2013'
    dt = datetime.strptime(day, '%d/%b/%Y')
    start = dt - timedelta(days=dt.weekday())
    end = start + timedelta(days=6)