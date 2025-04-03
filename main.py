import Framing_Function
import Unpacking_Function
import BinToInt

ReceiveFile_path = ""
state = ""

#发送功能
def send_Data(control,Data,destinationaddress,sourceaddress,times):
    match control:
        case '\x10':
            #发送数据
            for bytes in Framing_Function.Framing_Function1(Data,destinationaddress,sourceaddress,times):
                print(format(bytes,'08b'),end='')
            print ()
            print("发送:", Framing_Function.Framing_Function1(Data,destinationaddress,sourceaddress,times))
        case '\x20':
            #发送应答
            print("发送:", Framing_Function.ACK_send(destinationaddress,sourceaddress,times))
            #print('你搞你妈呢')
        case '\x30':
            #发送拒绝
            print("发送:", Framing_Function.REJ_send(destinationaddress,sourceaddress,times))

#send_Data('\x10',"w操你妈了个逼d","192.168.30.102","192.168.30.110",1)
#send_Data('\x20',"","192.168.30.102","192.168.30.110",1)
#send_Data(Framing_Function.REJ,"","192.168.30.102","192.168.30.110",1)
#print("解包得:",Unpacking_Function.Unpacking_Function1(Framing_Function.Framing_Function1("w操你妈了个逼d","192.168.30.102","192.168.30.110",3)))
#print("解包得:",Unpacking_Function.Unpacking_Function1(Framing_Function.ACK_send("192.168.30.102","192.168.30.110",6)))
#print("解包得:",Unpacking_Function.Unpacking_Function1(Framing_Function.REJ_send("192.168.30.102","192.168.30.110",4))

#截取数据包
def receive_Data():
    bytes_recdata = b''
    bytes_data = Unpacking_Function.receive_binData()

    if bytes_data != False:
        for index,bytes in enumerate(bytes_data) :
            #寻找起始符
            if bytes == 126:#Framing_Function.BEGIN_FLAG:

                bytes_recdata += bytes.to_bytes(1,byteorder='big')

                if index+1 < len(bytes_data):
                    bytes_data2 = bytes_data[index+1:]
                else:
                    return "DataError"
                #开始截取数据包
                for index2,bytes2 in enumerate(bytes_data2):
                    #寻找结束符
                    if  bytes_data2[index2] == 126:#Framing_Function.END_FLAG:
                        bytes_recdata += bytes2.to_bytes(1,byteorder='big')
                        return bytes_recdata
                    else:
                        bytes_recdata += bytes2.to_bytes(1,byteorder='big')
                    #未找到截至符则返回错误
                    if index2 >=30:
                        return "DataError"
                
#接受数据包
def receive_Data_keyboard(bytes_rec_data):
    while True:
        if Unpacking_Function.Unpacking_Function1(bytes_rec_data) != False:
            (Data,K) = Unpacking_Function.Unpacking_Function1(bytes_rec_data)
            if Data == 0x20:
                return 0x20 , K+1
            elif Data == 0x30:
                return 0x30 , K
            else:
                return Data , K
        else :
            return False

#将接收到的数据包解包(没用)
def UnpackingRecData(File):
    if receive_Data(File) != False:
        bytes_rec_data = receive_Data(File)
        if Unpacking_Function.Unpacking_Function1(bytes_rec_data) != False:
            (Data,K) = Unpacking_Function.Unpacking_Function1(bytes_rec_data)
            if Data == 0x20:
                return 0x20 , K+1
            elif Data == 0x30:
                return 0x30 , K
            else:
                return Data , K
    else :
        return False

#定义状态机(没什么用
def StateMachine():
    while state != "end" :
        if state == "leisure":
            if receive_Data(ReceiveFile_path) == "noData":
                state = "leisure"
            if receive_Data(ReceiveFile_path) != "noData":
                state = "receive"
        if state == "send":
            #发送数据
            print('发送')

        if state == "receive":
            #接收数据
            print('接收')

#print(receive_Data_keyboard(receive_Data()))


Data = input("请输入数据: ")
#Data = "w操你妈了个逼d操你妈了个逼的我操"
bytes_Data = Data.encode('gbk')
DataLength = len(bytes_Data)
print("数据长度:",DataLength)

def add_data(bytes_Data,K):
    i = 0
    data_tosend = "".encode('gbk')
    datalen = len(bytes_Data)
    while True:
        if i <= 15 and i < datalen:  
            if 0x81 <= bytes_Data[i] <= 0xFE:
                data_tosend += bytes_Data[i].to_bytes(1,byteorder='big')
                data_tosend += bytes_Data[i+1].to_bytes(1,byteorder='big')
                i += 2
            else:
                data_tosend += bytes_Data[i].to_bytes(1,byteorder='big')
                i += 1
            if i >= datalen or i>= 15:
                break
    send_Data('\x10',data_tosend,"192.168.30.211","192.168.20.102",K)
    #print(K)
    if i < datalen:
        add_data(bytes_Data[i:],K+1)
    
add_data(bytes_Data,1)
#receive_Data_keyboard(receive_Data())
#接受二进制数
print(receive_Data_keyboard(receive_Data()))
