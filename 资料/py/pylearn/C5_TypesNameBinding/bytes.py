buffer = b'abcdefghijklmn'
print(buffer,type(buffer),"len=",len(buffer))
print(buffer[2:9:2])

buffer = b'\x11\xff\x77'
print("%x" % (buffer[1]))

buffer = bytes(i+0x10 for i in range(10))
print(buffer)