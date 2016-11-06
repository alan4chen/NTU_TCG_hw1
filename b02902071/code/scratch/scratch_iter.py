
a = [1,2,3,4,5]
y = iter(a)
# print y()
print next(y, None)
print next(y, None)
print next(y, None)
print next(y, None)
print next(y, None) == None
print next(y, None) == None