from Queue import PriorityQueue


a = "35"


items = [3,1,2,-1]
pq = PriorityQueue()
for element in items:
        pq.put((element, a+str(element)))
print pq.get()
print pq.get()
print pq.get()
print pq.empty()
a, b =  pq.get()
print a
print b
print pq.empty()
print pq.get() == None
print pq.get()