import utils.stock_utils as su
import utils.calculate_utils as cu
from time import sleep
from manager.session_manager import SessionManager
from dao.financial_report_brief import FinancialReportBrief
from dao.stock_ex_rights_info import StockExRightsInfo

# 获取所有报告摘要
with SessionManager.get_session() as session:
    report_briefs = session.query(FinancialReportBrief.symbol, FinancialReportBrief.name).distinct().order_by(FinancialReportBrief.symbol.asc()).all()

for report_brief in report_briefs:
    print(report_brief.symbol)

    try:
        rights = su.stock_individual_ex_rights_detail(report_brief.symbol)
    except Exception as e:
        continue

    stock_ex_rights_info_list = []
    for ignore, right in rights.iterrows():
        rights_info = {
            'symbol': report_brief.symbol,
            'name': report_brief.name,
            'report_date': right["报告期"],
            'ex_rights_date': right["除权除息日"],
            'share_transfer_ratio': cu.get_nonnan_value(right["送转股份-送转总比例"], 0.0),
            'dividend_ratio': cu.get_nonnan_value(right["现金分红-现金分红比例"], 0.0),
            'dividend_yield': cu.get_nonnan_value(right["现金分红-股息率"], 0.0),
            'extra_info': "{}"
        }
        stock_ex_rights_info_list.append(rights_info)

    # 批量插入数据
    update_fields = ["name", "ex_rights_date", "share_transfer_ratio", "dividend_ratio", "dividend_yield", "extra_info"]
    StockExRightsInfo.batch_create(stock_ex_rights_info_list, update_fields)
    sleep(1)