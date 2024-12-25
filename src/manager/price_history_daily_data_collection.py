from dao.financial_report_brief import financial_report_brief
from dao.stock_price_history_daily import stock_price_history_daily
from datetime import datetime
import utils.stock_utils as su
import constant.fund_code_constant as fc
import constant.eastmoney_constant as const
import utils.date_utils as du
import utils.calculate_utils as cu
from time import sleep
from datetime import datetime, timedelta
from dao.financial_report_brief import financial_report_brief
from utils.util import group_list_by_fixed_length
import math

# 时间范围
START_DATE = "19880101"
END_DATE = datetime.now().strftime("%Y%m%d")
days = du.get_between_days(START_DATE, END_DATE)
days.sort()
# 1000天一组
dayChunks = group_list_by_fixed_length(days, 1000)


# 获取所有股票编码
report_briefs = financial_report_brief.select(financial_report_brief.symbol, financial_report_brief.name).distinct().order_by(financial_report_brief.symbol.asc()).execute()
for report_brief in report_briefs:
    print(report_brief.symbol)
    if report_brief.symbol <= "000991":
        continue
    for dayChunk in dayChunks:
        try:
            history_daily = su.stock_daily_history(report_brief.symbol, dayChunk[0].strftime("%Y%m%d"), dayChunk[-1].strftime("%Y%m%d"))
        except Exception as e:
            continue
        if history_daily is None:
            continue

        if len(history_daily) == 0:
            continue
        stock_history_list = []
        for ignore, hisotry in history_daily.iterrows():
            stock_history = stock_price_history_daily()
            stock_history.symbol = report_brief.symbol
            stock_history.name = report_brief.name
            stock_history.trade_date = hisotry.get("日期")
            stock_history.opening_price = hisotry.get("开盘")
            stock_history.closing_price = hisotry.get("收盘")
            stock_history.high_price = hisotry.get("最高")
            stock_history.low_price = hisotry.get("最低")
            stock_history.volume = hisotry.get("成交量")
            stock_history.turnover = hisotry.get("成交额")
            stock_history.amplitude = hisotry.get("振幅")
            stock_history.percentage_change = hisotry.get("涨跌幅")
            stock_history.price_change = hisotry.get("涨跌额")
            stock_history.turnover_rate = hisotry.get("换手率")
            stock_history.extra_info = "{}"
            stock_history_list.append(stock_history)
        
        stock_price_history_daily.bulk_create(stock_history_list, 1000)
        sleep(0.01)