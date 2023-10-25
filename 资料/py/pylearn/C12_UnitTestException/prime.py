#prime.py  v0.3
def isPrime(num):
   if num < 0 or num in (0,1):
      return  False    
   for i in range(2,num):
      if num % i == 0:
         return  False
   return True
