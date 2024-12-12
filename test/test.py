import utils.date_utils as du
import utils.stock_utils as su
import datetime
import akshare as ak

# date1 = datetime.datetime(2015, 1, 1).date()
# date2 = datetime.datetime(2017, 1, 1).date()

# date = datetime.datetime.strptime("2001-06-05", "%Y-%m-%d")

# # print(du.get_interval_days(date1, date2))

# ex_rights = su.stock_individual_ex_rights_detail("000651")
# print(ex_rights["送转股份-转股比例"])
# # print(ex_rights[ex_rights["除权除息日"] == date.date()].size)

# # print(ex_rights[ex_rights["除权除息日"] == date.date()].get("送转股份-转股比例").item())

# print(su.stock_daily_history("002304", "20150615", "20150620"))
# i = 0

# print(du.get_between_years(date1, date2))

# stock_add_stock_df = ak.stock_add_stock(symbol="600887")
# print(stock_add_stock_df)

# stock_history_dividend_df = ak.stock_history_dividend()
# print(len(stock_history_dividend_df[stock_history_dividend_df["代码"] == "600519"]))
# print(stock_history_dividend_df[stock_history_dividend_df["代码"] == "600887"].get("融资次数").item())

stock_cash_flow_sheet_by_yearly_em_df = ak.stock_cash_flow_sheet_by_yearly_em(symbol="sz000651")
# 购买固定资产、无形资产和其他长期资产支付的现金
# print(stock_cash_flow_sheet_by_yearly_em_df)
stock_cash_flow_sheet_by_yearly_em_df["long_asset_netcash_rate"] = stock_cash_flow_sheet_by_yearly_em_df["CONSTRUCT_LONG_ASSET"] / stock_cash_flow_sheet_by_yearly_em_df["TOTAL_OPERATE_INFLOW"]
print(stock_cash_flow_sheet_by_yearly_em_df[["CONSTRUCT_LONG_ASSET", "REPORT_DATE", "NETCASH_OPERATE", "TOTAL_OPERATE_INFLOW", "long_asset_netcash_rate"]])
# print(su.stock_2_date_2_cash_flow_info(["600519"]))