def bubbleSort(seq):
    for i in range(len(seq)-1 ,0 ,-1):
        for j in range(0,i):
            if seq[j] > seq[j+1]:
                seq[j],seq[j+1] = seq[j+1],seq[j]


seq = [3,9,1,4,7,6,5,8,2]
bubbleSort(seq)
print("Sorted:",seq)
