import utils.date_utils as du
import datetime

date1 = datetime.datetime(2023, 1, 1).date()
date2 = datetime.datetime(2023, 1, 15).date()

print(du.get_interval_days(date1, date2))