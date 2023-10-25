names = ['Tom', 'Andy', 'Alex', 'Dorothy']
print(list(enumerate(names)))

for idx, name in enumerate(names):
    print(name, "is at index", idx, "in the list.")