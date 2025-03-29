import Framing_Function
import Unpacking_Function

ReceiveFile_path = ""
state = ""

#发送功能
def send_Data(control,Data,destinationaddress,sourceaddress,times):
    match control:
        case '\x10':
            #发送数据
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

#在指定文件里接收二进制数据包
def receive_Data(File):
    i = 0
    while True:
        i += 1
        File.seek(i)
        if File.read(1) == b'\x7e':
            File.seek(i)
            while True:
                bytes_rec_data += File.read(1)
                if not File.read(1) :
                    return False
                if len(bytes_rec_data) >= 31 :
                    print("数据包过长或丢帧")
                    return False
                if bytes_rec_data[-1:] == b'\x7e' and bytes_rec_data[-2:-1] != b'\x7d':#转义字符
                    return bytes_rec_data
        if i >= 100 :
            return "noData"


#将接收到的数据包解包
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

#定义状态机
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













#Data = input("请输入数据: ")
Data = "w操你妈了个逼d你妈了个逼d你妈了个逼d你妈了个逼d你妈了个逼d"
bytes_Data = Data.encode('gbk')
DataLength = len(bytes_Data)
#print("数据长度:",DataLength)
i = 0
K = 0
while True:
    #发送逻辑
    if bytes_Data[i] == None:
        break
    K += 1
    while True:
        j = i
        data_tosend += bytes_Data[j]
        j += 1
        if j >=24 or bytes_Data[j] == None:
            break
    send_Data('\x10', data_tosend ,"192.168.30.102","192.168.30.110",K)
    if receive_Data(ReceiveFile_path) == (0x20 , K+1):
        data_tosend = None
        i=j+1
    
    




