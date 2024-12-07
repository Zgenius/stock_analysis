import utils.date_utils as du
import utils.stock_utils as su
import datetime

date1 = datetime.datetime(2015, 1, 1).date()
date2 = datetime.datetime(2017, 1, 1).date()

# date = datetime.datetime.strptime("2001-06-05", "%Y-%m-%d")

# # print(du.get_interval_days(date1, date2))

# ex_rights = su.stock_individual_ex_rights_detail("000651")
# print(ex_rights["送转股份-转股比例"])
# # print(ex_rights[ex_rights["除权除息日"] == date.date()].size)

# # print(ex_rights[ex_rights["除权除息日"] == date.date()].get("送转股份-转股比例").item())

# print(su.stock_daily_history("002304", "20150615", "20150620"))
# i = 0

print(du.get_between_years(date1, date2))