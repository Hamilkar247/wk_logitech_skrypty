import datetime 

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31)
    return date.replace(month=date.month+1, day=1) - datetime.timedelta(days=1)

print(str(last_day_of_month(datetime.date(2002,1,17))))

print(str(last_day_of_month(datetime.date(2002,12,17))))

print(str(last_day_of_month(datetime.date(2002,2,17))))

