import sys
import strategy.stock_back_testing as st

# 执行脚本
argv = sys.argv[1:]
testing = st.stock_back_testing()
testing.run(argv)