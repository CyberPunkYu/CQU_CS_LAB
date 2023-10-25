#zodiac.py
def myZodiac(year):
    zod = ['monkey','rooster','dog','pog','rat','ox','tiger',\
           'rabbit','dragon','snake','horse','sheep']  #生肖列表
    idx = year % 12
    return zod[idx]                                    #从列表中取第idx项
          
def main():
    y=eval(input("Please enter your year of birth:"))
    print("Your zodiac sign is:",myZodiac(y))

main()
    
