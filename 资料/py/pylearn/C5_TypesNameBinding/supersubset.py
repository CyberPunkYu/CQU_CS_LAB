#supersubset.py
s1 = {"CQU","NKU","THU","PKU"}
s2 = {"CQU","THU"}
print(s2.issubset(s1),s1.issubset(s2))  #s2是s1的子集，反过来不成立
print(s1.issuperset(s2),s2.issuperset(s1))  #s1是s2的超集，反过来不成立