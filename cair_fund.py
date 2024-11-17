import akshare as ak
from datetime import datetime
import pandas as pd

# 获取股票历史每天数据
def fund_daily_history(symbol_code, start_date, end_date):
    daily_history = ak.fund_etf_hist_em(symbol=symbol_code, period="daily", start_date=start_date, end_date=end_date, adjust="")
    daily_history['日期'] = pd.to_datetime(daily_history['日期'], format='%Y-%m-%d')
    daily_history['日期'] = daily_history['日期'].dt.date

    return daily_history