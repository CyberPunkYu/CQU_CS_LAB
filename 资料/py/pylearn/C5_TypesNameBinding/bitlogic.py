x = 0xaa
print("x =", bin(x))
print("x & 0x7f =", bin(x & 0x7f))
print("x | 0x77 =", bin(x | 0x77))

y = 0x00ff
y = y << 8
print("y =", hex(y))