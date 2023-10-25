#marriage.py
def match():
    girls = ['X','Y','Z']
    for a in girls:          #a - A的新娘的三种可能性
        for b in girls:      #b - B的新娘的三种可能性
            for c in girls:  #c - C的新娘的三种可能性
                #检查组合：A - a, B - b, C - c
                print("Check A-%s,B-%s,C-%s"%(a,b,c))
                if a!=b and b!= c and a!=c:
                    if a!='X' and c!='X' and c!='Z':
                	    print("Legal:A-%s,B-%s,C-%s" % (a,b,c)) #找到一种"合法"组合

match()