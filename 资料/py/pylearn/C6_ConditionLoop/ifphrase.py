sGender = input("Are you a boy or girl? (boy/girl):")
sGender = sGender.strip().lower()
iMarryAge = 22 if sGender == 'boy' else 20
print("Your legal marry age is:", iMarryAge, "in Mainland China.")