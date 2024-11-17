import cair_stock as cs
import sys

# "上证系列指数", "深证系列指数", "指数成份", "中证系列指数"
INDEX_FUND_LIST = ["上证系列指数", "深证系列指数", "指数成份", "中证系列指数"]
IDNEX_LEN = len(INDEX_FUND_LIST)
argv = sys.argv[1:]
if len(argv) != 0 and int(argv[0]) > 1 and int(argv[0]) <= IDNEX_LEN:
    index_fund_category = INDEX_FUND_LIST[int(argv[0]) - 1]
else:
    index_fund_category = "指数成份"


index_list = cs.index_list()

for index, row in index_list.iterrows():
    print(index, row["代码"], row["名称"])