sMonthName = input("Please input month name: ")
sMonthName = sMonthName.strip().title()
if sMonthName in ['January','March','May','July',
                  'August','October','December']:
    print("There are 31 days in the designated month.")
elif sMonthName in ['April', 'June','September', 'November']:
    print("There are 30 days in the designated month.")
elif sMonthName == "February" or sMonthName.startswith("Feb"):
    print("There are 28 or 29 days in the designated month.")
else:
    print("Unrecognized month name.")