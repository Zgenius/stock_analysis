import statsmodels.api as sm
import constant.constant as constant
from statsmodels.tsa.stattools import adfuller
import cair_stock as cs
import constant.eastmoney_constant as const
import strategy.MeanReversionStrategyBaseResiduals as mr
import time

FAILED = -1
SELL = 2
BUY = 1
HOLDING = 0

def index_fund_mean_reversion(symbol_code, start_date, end_date):
    # 获取给定基金的成分信息
    stocks = cs.index_contain_stocks(symbol_code);

    # 构造代码到信息的映射表
    stock_code_2_info = {}
    for index, row in stocks.iterrows():
        stock_code_2_info[row["成分券代码"]] = row

    # 获取股票编码
    stock_codes = list(stock_code_2_info.keys())
    stock_code_length = len(stock_codes)

    for i in range(0, stock_code_length - 1):
        for j in range(i + 1, stock_code_length):
            stock_code_a = stock_codes[i]
            stock_code_b = stock_codes[j]

            # 获取基础信息
            stock_daily_history_a = cs.stock_daily_history(stock_code_a, start_date, end_date)
            stock_daily_history_b = cs.stock_daily_history(stock_code_b, start_date, end_date)
            if len(stock_daily_history_a) <= constant.MIN_EXCHANGE_DAY_NUM or len(stock_daily_history_b) <= constant.MIN_EXCHANGE_DAY_NUM:
                continue

            stock_merge_list = cs.sync_data_list(stock_daily_history_a, stock_daily_history_b)
            stock_daily_history_a = stock_merge_list[0]
            stock_daily_history_b = stock_merge_list[1]

            # 元素数量
            length = len(stock_daily_history_a);
            # 没有数据，或者上市日期小于constant.MIN_EXCHANGE_DAY_NUM个交易日的就不计算了
            if length == 0 or length < constant.MIN_EXCHANGE_DAY_NUM:
                continue

            mean_reversion_code = mr.mean_reversion(stock_daily_history_a[const.CLOSE_PRICE_KEY], stock_daily_history_b[const.CLOSE_PRICE_KEY])
            if mean_reversion_code == -1:
                continue

            print(mean_reversion_code)
            print(stock_code_a, stock_code_2_info[stock_code_a]["成分券名称"], stock_code_b, stock_code_2_info[stock_code_b]["成分券名称"])

            # 睡眠100毫秒，防止请求过于频繁
            time.sleep(0.1)


# 基于残差的均值回归策略
def mean_reversion(stock1, stock2):
    # 对两只股票进行线性回归
    X = sm.add_constant(stock1)  # 添加常数项
    model = sm.OLS(stock2, X).fit()  # 线性回归
    residuals = model.resid  # 获取回归残差

    # ADF检验协整关系
    if (abs(residuals) < 1e-6).all():
        # print("Residuals are constant, skipping ADF test.")
        return -1

    # ADF检验协整关系
    adf_result = adfuller(residuals)
    # print(f"ADF检验的p值: {adf_result[1]}")

    # 判断是否具有协整关系
    if adf_result[1] < 0.05:
        print("两只股票具有协整关系。")
    else:
        # print("两只股票不具有协整关系。")
        return -1

    print(f"ADF检验的p值: {adf_result[1]}")

    # 计算价差（回归残差）
    spread = residuals

    # 计算价差的均值和标准差
    spread_mean = spread.mean()
    spread_std = spread.std()

    print("价差的均值:{:.15f}".format(spread_mean))
    # print(f"价差的均值: {spread_mean}")
    # print(f"价差的标准差: {spread_std}")
    print("价差的标准差:{:.15f}".format(spread_std))

    # 基于均值和标准差进行交易决策
    threshold_up = spread_mean + 2 * spread_std
    threshold_down = spread_mean - 2 * spread_std

    # 假设策略：当价差超过2倍标准差时买入/卖出
    if spread.get(spread.size - 1) > threshold_up:
        print("卖出信号：价差大于均值 + 2标准差")
        return 2
    elif spread.get(spread.size - 1) < threshold_down:
        print("买入信号：价差小于均值 - 2标准差")
        return 1
    else:
        print("没有信号，保持观望")
        return 0

# 下载两只股票的历史数据
def cointegrate(stock1, stock2):
    # 对两只股票进行线性回归
    X = sm.add_constant(stock1)  # 添加常数项
    model = sm.OLS(stock2, X).fit()  # 线性回归
    residuals = model.resid  # 获取回归残差

    # ADF检验协整关系
    if (abs(residuals) < 1e-6).all():
        print("Residuals are constant, skipping ADF test.")
        return False

    adf_result = adfuller(residuals)
    print(f"ADF检验的p值: {adf_result[1]}")

    # 判断是否具有协整关系
    if adf_result[1] < 0.05:
        res = True
        # print("两只股票具有协整关系。")
    else:
        res = False
        # print("两只股票不具有协整关系。")

    return res