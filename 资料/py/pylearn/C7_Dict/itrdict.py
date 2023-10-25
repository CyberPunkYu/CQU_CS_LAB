dora = {'id':'10003', 'name':'Dora Chen','gender':'female',\
        'age':32, 'title':'Sales'}

sText = "keys: "
for x in dora:
    sText += (str(x) + " - ")
print(sText)

print("dora.keys():", dora.keys())
print("type of dora.keys():",type(dora.keys()))

print("dora.values():", dora.values())
print("type of dora.values():",type(dora.values()))

print("key-value pairs:")
for k,v in dora.items():
    print("\t", k, "correspond to", v)
print("type of dora.items():", type(dora.items()))