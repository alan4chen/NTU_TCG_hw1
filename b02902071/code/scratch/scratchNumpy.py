import numpy as np
from collections import Counter

arr = np.zeros((3,4), dtype = 'int')
print arr
arr[1] = [1,2,3,4]
arr[2] = 99
print 99 in arr[1]
print Counter(np.where(arr==2)[0]).most_common()[0]