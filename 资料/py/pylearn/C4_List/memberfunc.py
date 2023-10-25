dummy = ['bob', 'henry', 'mary', 'bob', 'bob']
print("there are %d 'bob' in list." % (dummy.count('bob')))

dummy.clear()
print("list after clear:", dummy)

dummy.append('bob')
dummy.extend(['henry','mary'])

print("henry is found at index:", dummy.index('henry'))

dummy.remove('henry')
print("list after remove:", dummy)