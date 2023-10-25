import csv
# load file
filename='F:\\wj\\最优化\\GA\\cities.csv'
with open(filename) as f:
    reader=csv.reader(f)
    header_row=next(reader)
    cities=[]
    for row in reader:
       longti=float(row[1])
       lati=float(row[2])
       cities.append([longti,lati])


#GA

       