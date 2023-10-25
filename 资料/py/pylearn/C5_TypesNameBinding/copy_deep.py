import copy
chars = bytearray(b'abcdefghijklmn')
charsCopy = chars.copy()
charsCopy2 = chars[:]
print(id(chars),"-",id(charsCopy),"-",id(charsCopy2))

numbers = [0,1,2,3,4,5,6,7]
numbersCopy = numbers.copy()
numbersCopy2 = numbers[:]
numbersCopy3 = copy.copy(numbers)
numbersCopy4 = copy.deepcopy(numbers)
print(id(numbers),"-",id(numbersCopy),"-",id(numbersCopy2),
      "-",id(numbersCopy3),"-",id(numbersCopy4))