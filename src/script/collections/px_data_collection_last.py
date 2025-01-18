from model.stock_px_brief import StockPxBrief
from model.stock_basic_info import StockBasicInfo
import utils.stock_utils as su
import utils.calculate_utils as cu
from time import sleep
from datetime import datetime

def px_data_collection():
    # now = datetime.now().date()
    now = datetime(2025, 1, 3).date()
    # 获取所有股票编码
    stocks = StockBasicInfo.select(StockBasicInfo.symbol, StockBasicInfo.name).distinct().order_by(StockBasicInfo.symbol.asc()).all()

    for stock in stocks:
        try:
            data = su.stock_px_data(stock.symbol)
        except Exception as e:
            continue
        px_brief_list = []
        for ignore, record in data.iterrows():
            # 交易日小于当前日期则跳过
            # if record["数据日期"] < now:
                # continue

            px_brief = {
                'symbol': stock.symbol,
                'name': stock.name,
                'trade_date': record["数据日期"],
                'pe': cu.get_nonnan_value(record["PE(静)"], 0.0),
                'pe_ttm': cu.get_nonnan_value(record["PE(TTM)"], 0.0),
                'pb': cu.get_nonnan_value(record["市净率"], 0.0),
                'ps': cu.get_nonnan_value(record["市销率"], 0.0),
                'ps_ttm': cu.get_nonnan_value(record["市销率"], 0.0),
                'dv_ratio': 0.0,
                'dv_ttm': 0.0,
                'pcf': cu.get_nonnan_value(record["市现率"], 0.0),
                'peg': cu.get_nonnan_value(record["PEG值"], 0.0),
                'negotiable_shares': cu.get_nonnan_value(record["流通股本"], 0.0),
                'total_mv': cu.get_nonnan_value(record["总市值"], 0.0),
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
            'pcf',
            'peg',
            'negotiable_shares',
            'total_mv',
            'extra_info'
        ]
        StockPxBrief.batch_create(px_brief_list, update_fields)
        sleep(1)

if __name__ == "__main__":
    px_data_collection()
print("px_data_collection.py done")