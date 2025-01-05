import numpy as np

def parse_nan(data):
    for key, value in data.items():
        if isinstance(value, float) and np.isnan(value):
            data[key] = "nan"
    
    return data