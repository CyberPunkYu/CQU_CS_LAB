from matplotlib import patches

r = patches.Rectangle([0,0], 2, 1)
path = r.get_path()
print("vertices:\n",path.vertices)
print("codes:\n",path.codes)
