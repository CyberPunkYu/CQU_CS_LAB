def divide(a, b):
    return a/b


while True:
    sFirst = input("First number:")
    sSecond = input("Second number:")
    if sFirst == "q" or sSecond == "q":
        break
    try:
        iFirst = int(sFirst)
        iSecond = int(sSecond)
        fResult = divide(iFirst,iSecond)
    except (ZeroDivisionError) as e:
        print("You can not divide by 0:",e)
    except (ValueError,TypeError) as e:
        print("Illegal value been inputted:",e)
        print(type(e))
    except (Exception) as e:
        print("An exception found, I do not know how to process it.")
        raise
    else:
        
        print( sFirst, "/", sSecond, "=", fResult)
    finally:
        print("'Finally' will be executed what ever happens.")