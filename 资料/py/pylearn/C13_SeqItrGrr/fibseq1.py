#fibseq1.py
class Fibonacci:
    def __init__(self):
        self.seq = [0,1,1]					#序列第1项，第2项为1
        self.maxKey = 10000

    def computeTo(self,key):
        for idx in range(len(self.seq), key + 1):
            v = self.seq[idx - 1] + self.seq[idx - 2]
            self.seq.append(v)

    def __getitem__(self,key):
        if not isinstance(key,int):			#判断是否int类型
            raise TypeError
        if key <=0 or key > self.maxKey:	#数列不含第0项
            raise IndexError
        if key > len(self.seq):			
            self.computeTo(key)				#计算序列的前key项
        return self.seq[key]

    def __setitem__(self,key,value):		#key为下标，value为值
        if not isinstance(key,int):			#判断是否int类型
            raise TypeError	
        if key <=0 or key > self.maxKey:	#数列不含第0项，不可超过10000项
            raise IndexError
        if key > len(self.seq):
            self.computeTo(key)				#计算的前key项
        self.seq[key] = value

    def __len__(self):
        return self.maxKey		#返回最大项数10000作为长度

f = Fibonacci()					#实例化Fibonacci类
print("f[20]=",f[20])			#取值，导致f.__getitem__(20)被执行
f[10] = "熊孩子"				 #赋值，导致f.__setitem__(10,"熊孩子")被执行	
for i in range(1,21):
    print(f[i],end=",")			#取值，导致f.__getitem__(i)被执行
print("")						#换行
print("Length of f:",len(f))	#len(f)导致f.__len__()被执行