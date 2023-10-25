
#import numpy as np

def opt_v(v,prev,i):
#求完成前i个任务的最优方案
#v：每个方案的收入数组
#prev:当前方案不选时，可选的前面方案
  
   opt=[0,0,0,0,0,0,0,0,0]
   optpath=[[],[],[],[],[],[],[],[],[]]
   #opt(0)=0
   opt_path=[]
   for k in range(1,i+1):
       A=v[k]+opt[prev[k]]#选
       B=opt[k-1]#不选
       maxv=max(A,B)
       opt[k]=maxv
       
       if maxv==A:  #选
          optpath[k]=[k]+optpath[prev[k]]
       else: #不选
          optpath[k]=optpath[k-1]

       print(k,maxv,optpath[k])

v=[0,5,1,8,4,6,3,2,4]
prev=[0,0,0,0,1,0,2,3,5]
opt_v(v,prev,8)
