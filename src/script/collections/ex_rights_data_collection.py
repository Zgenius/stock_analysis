import utils.stock_utils as su
import utils.calculate_utils as cu
import pandas as pd
from time import sleep
from model.stock_basic_info import StockBasicInfo
from model.stock_ex_rights_info import StockExRightsInfo

# 分红除权等信息的数据收集
def ex_rights_data_collection():
    # 获取所有报告摘要
    report_briefs = StockBasicInfo.select(StockBasicInfo.symbol, StockBasicInfo.name).distinct().order_by(StockBasicInfo.symbol.asc()).all()

    for report_brief in report_briefs:
        try:
            rights = su.stock_individual_ex_rights_detail(report_brief.symbol)
        except Exception as e:
            continue

        stock_ex_rights_info_list = []
        for ignore, right in rights.iterrows():
            # 除权除息日为空则跳过
            if pd.isna(right["除权除息日"]):
                continue

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

if __name__ == "__main__":
    ex_rights_data_collection()