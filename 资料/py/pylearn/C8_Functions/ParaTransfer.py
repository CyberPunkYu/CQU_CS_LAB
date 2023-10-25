#ParaTransfer.py                             
def swap(x,y):                               
    print("in function:","id(x)=",id(x),"id(y)=",id(y))         
    x,y = y,x                                  
    s = x+y                                    
    print("x,y swap:","id(x)=",id(x),"id(y)=",id(y))       
    return s                                 
                                             
a,b = eval(input("input a and b(a,b):"))       
print("before function call:","id(a)=",id(a),"id(b)=",id(b))   
c = swap(a,b)                                  
print("after function call:","id(a)=",id(a),"id(b)=",id(b))    
print("a=%d,b=%d,c=%d"%(a,b,c))              