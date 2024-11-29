import akshare as ak
from datetime import datetime

stock_a_indicator_lg_df = ak.stock_a_indicator_lg(symbol="600036")
# print(stock_a_indicator_lg_df)

date = datetime.strptime("2012-04-09", "%Y-%m-%d").date()
# print(date)

print(stock_a_indicator_lg_df[stock_a_indicator_lg_df["trade_date"] == date].get("ps_ttm").item())