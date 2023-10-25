iAge = int(input("How old are you?"))
sGender = input("Are you a boy or girl(boy/girl)? ")
if sGender=="boy":
    if iAge >= 22:
        print("You are legal to get marry.")
    else:
        print("You are still too young.")
elif sGender=="girl":
    if iAge >= 20:
        print("You are legal to get marry.")
    else:
        print("You are still too young.")
else:
    print("Unrecognized gender, it should be 'boy' or 'girl'.")