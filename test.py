import numpy as np

bytes_num = b'\x01'

print(int.from_bytes(bytes_num,byteorder='big'))