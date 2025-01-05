import json
import math
import numpy as np

class JsonEncoder(json.JSONEncoder):
    def default(self, constant):
        if np.isnan(constant):
            return 'nan'
        elif constant == 'Infinity':
            return 'Positive Infinity'
        elif constant == '-Infinity':
            return 'Negative Infinity'
        elif constant is None:
            return ""
        return super().default(constant)

def parse_json(data):
    return json.dumps(data, ensure_ascii=False)