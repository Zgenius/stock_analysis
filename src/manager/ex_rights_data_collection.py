from dao.financial_report_brief import FinancialReportBrief
from dao.stock_ex_rights_info import StockExRightsInfo
from datetime import datetime
from time import sleep
from datetime import datetime, timedelta
from dao.financial_report_brief import FinancialReportBrief
from utils.util import group_list_by_fixed_length
import utils.stock_utils as su
import constant.fund_code_constant as fc
import constant.eastmoney_constant as const
import utils.date_utils as du
import utils.calculate_utils as cu
import math


report_briefs = FinancialReportBrief.select(FinancialReportBrief.symbol, FinancialReportBrief.name).distinct().order_by(FinancialReportBrief.symbol.asc()).execute()
for report_brief in report_briefs:
    print(report_brief.symbol)

    try:
        rights = su.stock_individual_ex_rights_detail(report_brief.symbol)
    except Exception as e:
        continue

    stock_ex_rights_info_list = []
    for ignore, right in rights.iterrows():
        rights_info = StockExRightsInfo()
        rights_info.symbol = report_brief.symbol
        rights_info.name = report_brief.name
        rights_info.report_date = right["报告期"]
        rights_info.ex_rights_date = right["除权除息日"]
        rights_info.share_transfer_ratio = cu.get_nonnan_value(right["送转股份-送转总比例"], 0.0)
        rights_info.dividend_ratio = cu.get_nonnan_value(right["现金分红-现金分红比例"], 0.0)
        rights_info.dividend_yield = cu.get_nonnan_value(right["现金分红-股息率"], 0.0)
        rights_info.extra_info = "{}"

        stock_ex_rights_info_list.append(rights_info)
    
    StockExRightsInfo.bulk_create(stock_ex_rights_info_list)
    sleep(1)