#basicset.py
countries = {"China","USA","Japan","France"}
countries.add("Italy")
countries.remove("Japan")
print("Set countries:",countries,"length=",len(countries))
print("Germany in set countries?", "Germany" in countries)

print("--------------------------------------------")
for x in countries:
    print(x)

numbers = {12,5,6,90,15}
print("max,min,sum of numbers:",max(numbers),min(numbers),sum(numbers))
numbers.pop()
print("Numbers after pop:", numbers)

s1 = {"CQU","NKU","THU","PKU"}
s2 = {"PKU","CQU","THU","NKU"}
print("s1 = s2 ?", s1==s2)