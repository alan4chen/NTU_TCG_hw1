def intersect(a, b):
    return list(set(a) & set(b))

b1 = [1,2,3,4,5,9,11,15]
b2 = [4,5,6,7,8]
b3 = intersect(b1, b2)

print map(lambda x: x+1, b1)