import numpy as np

mylist = [1,0,1,0,0,0,0,1,1,0,1,0,0,1,1,0]
good, bad = [], []
for x in mylist:
    (bad, good)[x == 1].append(x)

print(bad)
print(good)

