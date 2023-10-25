dora = {'id':'10003', 'name':'Dora Chen','gender':'female',\
        'age':32, 'title':'Sales'}

sTitle = dora.pop('title')
print("value of the poppped item:", sTitle)

dora.popitem()
print("dict dora: ", dora)