import numpy as np

def bin_to_int(data):
    data_int = 0
    for i in range(len(data)):
        if data[i] == '1':
            data_int += 2**(len(data) - i - 1)
        elif data[i] == '0':
            data_int += 0
    return data_int