x = 65534
bufferLittle = x.to_bytes(2, 'little')
print("little endian:", bufferLittle)
bufferBig = x.to_bytes(2,'big')
print("big endian:", bufferBig)

y = int.from_bytes(b'\xfe\xff','little')
print(y)