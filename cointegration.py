import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller

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