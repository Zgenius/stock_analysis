from dao.financial_report_brief import FinancialReportBrief
from dao.stock_price_history_daily import StockPriceHistoryDaily
import utils.stock_utils as su
import utils.date_utils as du
import utils.calculate_utils as cu
from time import sleep
from datetime import datetime
from manager.session_manager import SessionManager
from utils.util import group_list_by_fixed_length

# 时间范围
START_DATE = "19880101"
END_DATE = datetime.now().strftime("%Y%m%d")
days = du.get_between_days(START_DATE, END_DATE)
days.sort()
# 1000天一组
dayChunks = group_list_by_fixed_length(days, 1000)

# 获取所有股票编码
with SessionManager.get_session() as session:
    report_briefs = session.query(FinancialReportBrief.symbol, FinancialReportBrief.name).distinct().order_by(FinancialReportBrief.symbol.asc()).all()

for report_brief in report_briefs:
    print(report_brief.symbol)
    for dayChunk in dayChunks:
        try:
            history_daily = su.stock_daily_history(report_brief.symbol, dayChunk[0].strftime("%Y%m%d"), dayChunk[-1].strftime("%Y%m%d"))
        except Exception as e:
            continue
        if history_daily is None or len(history_daily) == 0:
            continue

        stock_history_list = []
        for ignore, history in history_daily.iterrows():
            stock_history = {
                'symbol': report_brief.symbol,
                'name': report_brief.name,
                'trade_date': history.get("日期"),
                'opening_price': history.get("开盘"),
                'closing_price': history.get("收盘"),
                'high_price': history.get("最高"),
                'low_price': history.get("最低"),
                'volume': history.get("成交量"),
                'turnover': history.get("成交额"),
                'amplitude': history.get("振幅"),
                'percentage_change': history.get("涨跌幅"),
                'price_change': history.get("涨跌额"),
                'turnover_rate': history.get("换手率"),
                'extra_info': "{}"
            }
            stock_history_list.append(stock_history)
        
        # 批量插入并在冲突时更新
        update_fields = [
            'name',
            'opening_price',
            'closing_price',
            'high_price',
            'low_price',
            'volume',
            'turnover',
            'amplitude',
            'percentage_change',
            'price_change',
            'turnover_rate',
            'extra_info'
        ]
        StockPriceHistoryDaily.batch_create(stock_history_list, update_fields)
        sleep(0.01)