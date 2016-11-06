import numpy as np

arr = np.zeros((3,4), dtype = 'bool')
arr[2][1] = True

arr2 = np.zeros((3,4), dtype = 'bool')
arr2[2][1] = True
# print (arr == arr2).all()

print "--"

print zip(np.where(arr == False)[0], np.where(arr == False)[1])
# print len(np.where(arr == True)[0])