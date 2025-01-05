import json
import math
from utils.dict_utils import parse_nan

# 示例字典，包含 NaN 和 Inf
data = {
    "value1": 123.45,
    "value2": float('nan'),  # NaN值
    "value3": 678.90,
    "value4": float('inf')   # Inf值
}

print(parse_nan(data))