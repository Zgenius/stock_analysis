from model.stock_px_brief import StockPxBrief
from model.stock_basic_info import StockBasicInfo
import utils.stock_utils as su
import utils.calculate_utils as cu
from time import sleep
from datetime import datetime

def px_data_collection():
    now = datetime.now().date()
    # 获取所有股票编码
    stocks = StockBasicInfo.select(StockBasicInfo.symbol, StockBasicInfo.name).distinct().order_by(StockBasicInfo.symbol.asc()).all()

    for stock in stocks:
        try:
            data = su.stock_individual_indicator(stock.symbol)
        except Exception as e:
            continue
        px_brief_list = []
        for ignore, record in data.iterrows():
            # 交易日小于当前日期则跳过
            if record["trade_date"] < now:
                continue

            px_brief = {
                'symbol': stock.symbol,
                'name': stock.name,
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

if __name__ == "__main__":
    px_data_collection()
print("px_data_collection.py done")