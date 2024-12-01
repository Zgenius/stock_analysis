from datetime import datetime, timedelta

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