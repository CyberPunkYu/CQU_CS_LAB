#nummagic.py
card1 = """Card 1:
    1 11 21 31 41 51
    3 13 23 33 43 53
    5 15 25 35 45 55
    7 17 27 37 47 57
    9 19 29 39 49 59"""

card2 = """Card 2:
    2 11 22 31 42 51
    3 14 23 34 43 54
    6 15 26 35 46 55
    7 18 27 38 47 58
   10 19 30 39 50 59"""

card3 = """Card 3:
    4 13 22 31 44 53
    5 14 23 36 45 54
    6 15 28 37 46 55
    7 20 29 38 47 60
   12 21 30 39 52 *"""
    
card4 = """Card 4:
    8 13 26 31 44 57
    9 14 27 40 45 58
   10 15 28 41 46 59
   11 24 29 42 47 60
   12 25 30 43 56 *"""

card5 = """Card 5:
   16 21 26 31 52 57
   17 22 27 48 53 58
   18 23 28 49 54 59
   19 24 29 50 55 60
   20 25 30 51 56 *"""

card6 = """Card 6:
   32 37 42 47 52 57
   33 38 43 48 53 58
   34 39 44 49 54 59
   35 40 45 50 55 60
   36 41 46 51 56 *"""

sQuestion = "\nIs your number in this card? y for yes, n for no:"
b1 = 1 if input(card1+sQuestion).lower().strip() == 'y' else 0 
b2 = 1 if input(card2+sQuestion).lower().strip() == 'y' else 0
b3 = 1 if input(card3+sQuestion).lower().strip() == 'y' else 0
b4 = 1 if input(card4+sQuestion).lower().strip() == 'y' else 0
b5 = 1 if input(card5+sQuestion).lower().strip() == 'y' else 0
b6 = 1 if input(card6+sQuestion).lower().strip() == 'y' else 0

print("Binary answer:",b6,b5,b4,b3,b2,b1)
print("The number is:", b6*32 + b5*16 + b4*8 + b3*4 + b2*2 + b1*1)
