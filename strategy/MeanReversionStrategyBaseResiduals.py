import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

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

    print(f"价差的均值: {spread_mean}")
    print(f"价差的标准差: {spread_std}")

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