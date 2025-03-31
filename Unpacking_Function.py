import Framing_Function

#接受二进制数
def receive_binData():
    data = 0b1111100100110011
    bytes_data = data.to_bytes(data.bit_length()//8, byteorder='big')
    print("字节数据:", bytes_data)
    return data

#将二进制数转换为bytes类型
def int_to_bytes(n):
    print("")

#对CRC校验位前的数据进行CRC校验
def CRC_Check(bytes_Data):
    bytes_crc16bit = Framing_Function.crc_calculation(bytes_Data[:-3])
    if bytes_crc16bit == bytes_Data[-3:-1]:
        #print("CRC校验成功")
        return True
    else:
        #print("CRC校验失败")
        return False

#对数据进行解包,
def Unpacking_Function1(bytes_Data):
    if CRC_Check(bytes_Data) :
        bytes_Data1 = bytes_Data[:-3]
        if int.from_bytes(bytes_Data1[-1:],byteorder= 'big' ) & 0xF0 == 0x10:
            #print("数据帧")
            bytes_senddata = bytes_Data1[11:-1]
            bytes_Knum = int.from_bytes(bytes_Data1[-1:],byteorder= 'big')& 0x0F

            return (bytes_senddata.decode('gbk'), bytes_Knum)
        
        if int.from_bytes(bytes_Data1[-1:],byteorder= 'big' )& 0xF0 == 0x20:
            #print("应答帧:",int.from_bytes(bytes_Data1[-1:],byteorder= 'big')& 0x0F)

            return (0x20,int.from_bytes(bytes_Data1[-1:],byteorder= 'big')& 0x0F)
        
        if int.from_bytes(bytes_Data1[-1:],byteorder= 'big' )& 0xF0 == 0x30:
            #print("拒绝帧:",int.from_bytes(bytes_Data1[-1:],byteorder= 'big')& 0x0F)
            
            return (0x30,int.from_bytes(bytes_Data1[-1:],byteorder= 'big')& 0x0F)
        else:
            print("数据帧错误")
            return False
    else:
        print("CRC校验失败")
        return False


receive_binData()