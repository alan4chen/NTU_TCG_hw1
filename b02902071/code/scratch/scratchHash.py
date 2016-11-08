import cPickle
import hashlib
m = hashlib.md5()
m.update("Nobody inspects")
b = m.digest()

m.update(cPickle.dumps(['a','b']))
c = m.digest()
print c==b