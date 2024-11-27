import strategy.stock_back_testing as st

# 用来制定代码进行均值回归计算
stock_pair_list = [
    # 招商银行，宁波银行
    [
        "600036", "002142"
    ],
    # 格力电器，美的集团
    [
        "000651", "000333"
    ],
    # 泸州老窖，五粮液
    [
        "000568", "000858"
    ],
    # 中国神华，陕西煤业
    [
        "601088", "601225"
    ]
]

for stock_code_pair in stock_pair_list:
    stock_back = st.stock_back_testing()
    stock_back.run(stock_code_pair)
    split = ""
    for i in range(0, 100):
        split += "="
    print(split)
