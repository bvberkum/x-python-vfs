
import datrie


dt = datrie.Trie('0123456789abcdefghijklmnopqrstuvwxyz-:./')



# create a dictionary with 30k entries
#d = {str(x):str(x) for x in xrange(1, 30001)}
#query = '108'
#for key, val in d.iteritems():
#    dt[unicode(key)] = val
#
#print d
#print dt


import os

i=1

dt[u'foo'] = i
dt[u'foo/bar'] = i
dt[u'frob'] = i
dt[u'baz/1'] = i
dt[u'baz/2'] = i
dt[u'baz/3'] = i

print dt

print dt.keys(u'f')
print dt.keys(u'baz')


print dt.keys(u'baz/34')


