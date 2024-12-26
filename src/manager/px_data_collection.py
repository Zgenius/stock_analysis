from dao.stock_basic_info import StockBasicInfo
from dao.stock_px_brief import StockPxBrief
from dao.financial_report_brief import FinancialReportBrief
from datetime import datetime
import utils.stock_utils as su
import constant.fund_code_constant as fc
import constant.eastmoney_constant as const
import utils.date_utils as du
import utils.calculate_utils as cu
from time import sleep
from datetime import datetime, timedelta
from dao.financial_report_brief import FinancialReportBrief
import math

# 获取所有股票编码
report_briefs = FinancialReportBrief.select(FinancialReportBrief.symbol, FinancialReportBrief.name).distinct().order_by(FinancialReportBrief.symbol.asc()).execute()
for report_brief in report_briefs:
    print(report_brief.symbol)
    px_brief_list = []
    try:
        data = su.stock_individual_indicator(report_brief.symbol)
    except Exception as e:
        continue
    for ignore, record in data.iterrows():
        px_brief = StockPxBrief()
        px_brief.symbol = report_brief.symbol
        px_brief.name = report_brief.name
        px_brief.trade_date = record["trade_date"]
        px_brief.pe = cu.get_nonnan_value(record["pe"], 0.0)
        px_brief.pe_ttm = cu.get_nonnan_value(record["pe_ttm"], 0.0)
        px_brief.pb = cu.get_nonnan_value(record["pb"], 0.0)
        px_brief.ps = cu.get_nonnan_value(record["ps"], 0.0)
        px_brief.ps_ttm = cu.get_nonnan_value(record["ps_ttm"], 0.0)
        px_brief.dv_ratio = cu.get_nonnan_value(record["dv_ratio"], 0.0)
        px_brief.dv_ttm = cu.get_nonnan_value(record["dv_ttm"], 0.0)
        px_brief.total_mv = cu.get_nonnan_value(record["total_mv"], 0.0)
        px_brief.extra_info = "{}"
        px_brief_list.append(px_brief)
    
    try:
        StockPxBrief.bulk_create(px_brief_list, 1000)
    except Exception as e:
        continue
    sleep(0.1)