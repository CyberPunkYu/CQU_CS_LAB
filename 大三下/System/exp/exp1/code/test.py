import serial

serialPort = "COM4"
baudRate = 9600
ser = serial.Serial(serialPort, baudRate, timeout = 0.5)

demo0 = b"0"
demo1 = b"1"

while 1:
    str = ser.readline() # 接收下位机上传的
    print(str)
    x = int(input("请输入0 or 1："))
    if(x == 1):
        ser.write(demo1) # 发送字节1
    else:
        ser.write(demo0) # 发送字节0
ser.close()