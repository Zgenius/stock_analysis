import utils.stock_utils as su
from model.statement_of_financial_position import StatementOfFinancialPosition
from model.stock_basic_info import StockBasicInfo
from utils.json_utils import parse_json
from time import sleep
from datetime import datetime
from utils.dict_utils import parse_nan

def financialposition_data_collection():
    now = datetime.now().date()
    # 获取所有股票编码
    stocks = StockBasicInfo.select(StockBasicInfo.symbol, StockBasicInfo.name).distinct().order_by(StockBasicInfo.symbol.asc()).all()

    for stock in stocks:
        if stock.symbol == '600519':
            continue

        try:
            data = su.stock_statement_of_financial_position(stock.symbol)
        except Exception as e:
            continue
        financial_position_list = []
        for ignore, record in data.iterrows():
            # 交易日小于当前日期则跳过 TODO 记得打开
            # if record["report_date"] < now:
            #     continue

            # 这里将nan转成字符串，要不数据库没办法存储
            record_dict = parse_nan(record.to_dict())

            financial_position = {
                'symbol': stock.symbol,
                'name': stock.name,
                'report_date': record["REPORT_DATE"],
                'extra_info': parse_json(record_dict)
            }
            financial_position_list.append(financial_position)

        if len(financial_position_list) == 0:
            continue
        
        # 批量插入并在冲突时更新
        update_fields = ['name', 'report_date', 'extra_info']
        StatementOfFinancialPosition.batch_create(financial_position_list, update_fields)
        sleep(0.1)

if __name__ == "__main__":
    financialposition_data_collection()
print("financialposition_data_collection.py done")