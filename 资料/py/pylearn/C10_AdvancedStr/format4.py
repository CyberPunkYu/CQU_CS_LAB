#format4.py
print("pi = {pi:010.2f}, {pi:<10.2f}, "
      "{pi:^10.2f},{pi:@>10.2f}".format(pi=3.1415926535497932))
print("pi = {0:+10.2f}, {1:=+10.2f}".format(3.14159,3.14159))