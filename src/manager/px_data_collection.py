from dao.stock_px_brief import StockPxBrief
from dao.financial_report_brief import FinancialReportBrief
import utils.stock_utils as su
import utils.calculate_utils as cu
from time import sleep
from manager.session_manager import SessionManager

# 获取所有股票编码
report_briefs = SessionManager.query(FinancialReportBrief.symbol, FinancialReportBrief.name).distinct().order_by(FinancialReportBrief.symbol.asc()).all()

for report_brief in report_briefs:
    print(report_brief.symbol)
    try:
        data = su.stock_individual_indicator(report_brief.symbol)
    except Exception as e:
        continue
    px_brief_list = []
    for ignore, record in data.iterrows():
        px_brief = {
            'symbol': report_brief.symbol,
            'name': report_brief.name,
            'trade_date': record["trade_date"],
            'pe': cu.get_nonnan_value(record["pe"], 0.0),
            'pe_ttm': cu.get_nonnan_value(record["pe_ttm"], 0.0),
            'pb': cu.get_nonnan_value(record["pb"], 0.0),
            'ps': cu.get_nonnan_value(record["ps"], 0.0),
            'ps_ttm': cu.get_nonnan_value(record["ps_ttm"], 0.0),
            'dv_ratio': cu.get_nonnan_value(record["dv_ratio"], 0.0),
            'dv_ttm': cu.get_nonnan_value(record["dv_ttm"], 0.0),
            'total_mv': cu.get_nonnan_value(record["total_mv"], 0.0),
            'extra_info': "{}"
        }
        px_brief_list.append(px_brief)
    
    if len(px_brief_list) == 0:
        continue
    
    # 批量插入并在冲突时更新
    update_fields = [
        'name',
        'trade_date',
        'pe',
        'pe_ttm',
        'pb',
        'ps',
        'ps_ttm',
        'dv_ratio',
        'dv_ttm',
        'total_mv',
        'extra_info'
    ]
    StockPxBrief.batch_create(px_brief_list, update_fields)
    sleep(0.1)