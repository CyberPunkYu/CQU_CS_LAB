

#正则表达式：字符串模式 （判断字符串是否符合一定的标准

import re
# 创建模式对象

# pat = re.compile("AA") # 此出的AA，是正则表达式，用来去验证其他的字符串
#m = pat.search("CBA")   #search字符串被校验的内容

#m = pat.search("ABCAA")
#m = pat.search("AABCAADDCCAAA")    #search方法，进行比对查找

#没有模式对象
# m = re.search("asd","Aasd")     #前面的字符串是规则（模板），后面的字符串是被校验的对象
# print(m)


print(re.findall("a","ASDaDFGAa"))      #前面字符串是规则（正则表达式），后面字符串是被校验的字符串

#print(re.findall("[A-Z]","ASDaDFGAa"))

#print(re.findall("[A-Z]+","ASDaDFGAa"))


#sub

# print(re.sub("a","A","abcdcasd"))   #找到a用A替换，在第三个字符串中查找"A"
#
# #建议在正则表达式中，被比较的字符串前面加上r，不用担心转义字符的问题
# a = r"\aabd-\'"
# print(a)