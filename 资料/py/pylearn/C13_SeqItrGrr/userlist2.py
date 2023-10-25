class UserList(list):
    def __init__(self,*args):
        super().__init__(*args)
        self.iCounter = 0

    def __getitem__(self, idx):
        self.iCounter += 1
        return super().__getitem__(idx)

a = UserList()
a.extend([0,1,2,3,4,5,6,7,8,9])
a[3] = "熊孩子"
print("a[2]=",a[2],"len(a)=",len(a))
print("a[3]=",a[3])
print("a.iCounter=",a.iCounter)
