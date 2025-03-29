import numpy as np
import socket
import struct
import zlib

SENT_DATA = b'\x10'
ACK = b'\x20'
REJ = b'\x30'
BEGIN_FLAG = b'\x7e'
END_FLAG = b'\x7e'
ESCAPE_FLAG = b'\x7d'

#计算CRC16校验码
def crc_calculation(Data):
    crc_full = zlib.crc32(Data)
    crc_16bit = crc_full & 0xffff
    bytes_crc16bit = crc_16bit.to_bytes(2,byteorder='big')
    return bytes_crc16bit

#数据包成帧
def Framing_Function1(bytes_Data,destinationaddress,sourceaddress,times):
    #bytes_Data = Data.encode('gbk')
    bytes_destinationaddress = socket.inet_aton(destinationaddress)
    bytes_sourceaddress = socket.inet_aton(sourceaddress)

    DataLength = len(bytes_Data)
    bytes_DataLength = DataLength.to_bytes(2,byteorder='big')
    #bytes_times = times.to_bytes(1,byteorder='big')
    bytes_senddata=(0x10+times).to_bytes(1,byteorder='big')
    bytes_after1_Data = BEGIN_FLAG + bytes_destinationaddress + bytes_sourceaddress + bytes_DataLength + bytes_Data + bytes_senddata
    bytes_crc16bit = crc_calculation(bytes_after1_Data)
    bytes_after2_Data = bytes_after1_Data + bytes_crc16bit + END_FLAG
    return bytes_after2_Data

#发送应答帧
def ACK_send(destinationaddress,sourceaddress,times):

    bytes_destinationaddress = socket.inet_aton(destinationaddress)
    bytes_sourceaddress = socket.inet_aton(sourceaddress)
    bytes_DataLength = b'\x00'

    bytes_ACK = (0x20+times).to_bytes(1,byteorder='big')
    bytes_after1_Data = BEGIN_FLAG + bytes_destinationaddress + bytes_sourceaddress + bytes_DataLength + bytes_ACK
    bytes_crc16bit = crc_calculation(bytes_after1_Data)
    bytes_after2_Data = bytes_after1_Data + bytes_crc16bit + END_FLAG
    return bytes_after2_Data

#发送拒绝帧
def REJ_send(destinationaddress,sourceaddress,times):

    bytes_destinationaddress = socket.inet_aton(destinationaddress)
    bytes_sourceaddress = socket.inet_aton(sourceaddress)
    bytes_DataLength = b'\x00'

    bytes_REJ = (0x30+times).to_bytes(1,byteorder='big')
    bytes_after1_Data = BEGIN_FLAG + bytes_destinationaddress + bytes_sourceaddress + bytes_DataLength + bytes_REJ
    bytes_crc16bit = crc_calculation(bytes_after1_Data)
    bytes_after2_Data = bytes_after1_Data + bytes_crc16bit + END_FLAG
    return bytes_after2_Data
