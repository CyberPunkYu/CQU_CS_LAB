buffer = bytearray(0x00 for x in range(10))
print(type(buffer), buffer)

buffer = bytearray(b'abcdefghijklmn')
buffer[1] = ord('B')
print(buffer)
print(buffer[3:11:3])