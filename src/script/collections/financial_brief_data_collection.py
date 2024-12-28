from model.financial_report_brief import FinancialReportBrief
from time import sleep
from datetime import datetime
import utils.stock_utils as su
import utils.date_utils as du
import utils.calculate_utils as cu


def financial_brief_data_collection():
    now = datetime.now()
    # 财报日期
    annual_report_dates = du.get_report_dates(now, 0)

    for date in annual_report_dates:
        # 获取财务数据基础信息
        stock_code_2_date_2_base_info = su.stock_2_date_base_info([date])
        if stock_code_2_date_2_base_info is None or len(stock_code_2_date_2_base_info) == 0:
            continue
        
        brief_list = []
        for symbol, date2row in stock_code_2_date_2_base_info.items():
            for row in date2row.values():
                brief = {
                    'symbol': symbol,
                    'name': row.get("股票简称"),
                    'report_time': datetime.strptime(date, "%Y%m%d"),
                    'operating_revenue': cu.get_nonnan_value(row.get("营业收入-营业收入"), 0.0),
                    'net_profit': cu.get_nonnan_value(row.get("净利润-净利润"), 0.0),
                    'net_asset_value_per_share': cu.get_nonnan_value(row.get("每股净资产"), 0.0),
                    'earnings_per_share': cu.get_nonnan_value(row.get("每股收益"), 0.0),
                    'operating_cash_flow_per_share': cu.get_nonnan_value(row.get("每股经营现金流量"), 0.0),
                    'return_on_equity': cu.get_nonnan_value(row.get("净资产收益率"), 0.0),
                    'gross_profit_ratio': cu.get_nonnan_value(row.get("销售毛利率"), 0.0),
                    'extra_info': "{}"
                }
                brief_list.append(brief)

        # 批量插入数据
        update_fields = ["name", "operating_revenue", "net_profit", "net_asset_value_per_share", "earnings_per_share", "operating_cash_flow_per_share", "return_on_equity", "gross_profit_ratio", "extra_info"]
        FinancialReportBrief.batch_create(brief_list, update_fields)
        sleep(0.01)

if __name__ == "__main__":
    financial_brief_data_collection()