import utils.stock_utils as su
from model.statement_of_cash_flows import StatementOfCashFlows
from model.stock_basic_info import StockBasicInfo
from utils.json_utils import parse_json
from time import sleep
from utils.dict_utils import parse_nan
from datetime import datetime, timedelta

def financial_cash_flows_data_collection():
    now = datetime.now().date()
    # 最近1年之前
    last_year_date = now - timedelta(days = 365)
    # 获取所有股票编码
    stocks = StockBasicInfo.select(StockBasicInfo.symbol, StockBasicInfo.name).distinct().order_by(StockBasicInfo.symbol.asc()).all()

    for stock in stocks:
        try:
            data = su.stock_statement_of_financial_position(stock.symbol)
        except Exception as e:
            continue
        cash_flows_list = []
        for ignore, record in data.iterrows():
            # 交易日小于当前日期则跳过
            if record["report_date"] < last_year_date:
                continue

            # 这里将nan转成字符串，要不数据库没办法存储
            record_dict = parse_nan(record.to_dict())

            cash_flows = {
                'symbol': stock.symbol,
                'name': stock.name,
                'report_date': record["REPORT_DATE"],
                'extra_info': parse_json(record_dict)
            }
            cash_flows_list.append(cash_flows)

        if len(cash_flows_list) == 0:
            continue
        
        # 批量插入并在冲突时更新
        update_fields = ['name', 'report_date', 'extra_info']
        StatementOfCashFlows.batch_create(cash_flows_list, update_fields)
        sleep(0.1)

if __name__ == "__main__":
    financial_cash_flows_data_collection()
print("financialposition_data_collection.py done")