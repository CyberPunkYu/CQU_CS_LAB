import json

dora = {"name":"Dora CHEN", "no":"2018173", "age":26,"married":False,
  "scores":[{"C++":76},{"Data Structure":99.5},{"Home Econoics":62}]}

#print(json.dumps(dora))
with open("dora.json","w") as f:
     json.dump(dora,f)

with open("dora.json") as f:
    doraLoaded = json.load(f)

for key,value in doraLoaded.items():
    print(key,":", value)