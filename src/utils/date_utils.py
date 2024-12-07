from datetime import datetime, timedelta

# 闰年判断函数
def is_leap_year(year):
    # 闰年判断函数
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

# 获取时间范围内的每一天
def get_between_days(start_date, end_date):
    if type(start_date) == str:
        start_date = datetime.strptime(start_date, "%Y%m%d")
    
    if type(end_date) == str:
        end_date = datetime.strptime(end_date, "%Y%m%d")

    days = []
    current_date = start_date
    while current_date <= end_date:
        days.append(current_date)
        current_date += timedelta(days=1)
    
    return days


# 通过字符串或者int获取datetime对象
def get_date(dateStr):
    if type(dateStr) == str:
        date = datetime.strptime(dateStr, "%Y%m%d")
    elif type(dateStr) == int:
        date = datetime.strptime(str(dateStr), "%Y%m%d")
    else:
        date = dateStr
    return date

# 获取两个时间差距多少天
def get_interval_days(start_date, end_date):
    return (end_date - start_date).days

# 获取时间范围内的每一天
def get_between_years(start_date, end_date):
    if type(start_date) == str:
        start_date = datetime.strptime(start_date, "%Y%m%d")
    
    if type(end_date) == str:
        end_date = datetime.strptime(end_date, "%Y%m%d")

    years = []
    current_date = start_date
    while current_date.year <= end_date.year:
        years.append(current_date)
        # 处理闰年的情况
        if is_leap_year(current_date.year):
            current_date += timedelta(days=366)
        else:
            current_date += timedelta(days=365)

    return years