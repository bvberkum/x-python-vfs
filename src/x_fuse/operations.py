from __future__ import with_statement, print_function
import os
import errno

from fuse import FuseOSError, Operations


def fsops_proxy(func):
    func_name = func.__name__
    def func_(self, path, *a):
        path_ = self._real_path(path)
        return getattr(self, func_name)(path_, *a)
    return func_

class AbstractProxy(Operations):

    def _real_path(self, partial):
        raise NotImplemented()

    @fsops_proxy
    def access(self, path, mode): pass
    @fsops_proxy
    def chmod(self, path, mode): pass
    @fsops_proxy
    def chown(self, path, uid, gid): pass
    @fsops_proxy
    def getattr(self, path, fh=None): pass
    @fsops_proxy
    def listxattr(self, path): pass
    @fsops_proxy
    def getxattr(self, path, name): pass
    @fsops_proxy
    def readdir(self, path, fh): pass
    @fsops_proxy
    def readlink(self, path): pass
    @fsops_proxy
    def mknod(self, path, mode, dev): pass
    @fsops_proxy
    def rmdir(self, path): pass
    @fsops_proxy
    def mkdir(self, path, mode): pass
    @fsops_proxy
    def statfs(self, path): pass
    @fsops_proxy
    def unlink(self, path): pass
    #def symlink(self, name, target):
    #def rename(self, old, new):
    #def link(self, target, name):
    @fsops_proxy
    def utimens(self, path, times=None): pass

    @fsops_proxy
    def open(self, path, flags): pass
    @fsops_proxy
    def create(self, path, mode, fi=None): pass
    @fsops_proxy
    def read(self, path, length, offset, fh): pass
    @fsops_proxy
    def write(self, path, buf, offset, fh): pass
    @fsops_proxy
    def truncate(self, path, length, fh=None): pass
    @fsops_proxy
    def flush(self, path, fh): pass
    @fsops_proxy
    def release(self, path, fh): pass
    @fsops_proxy
    def fsync(self, path, fdatasync, fh): pass


import datrie
class Composite(AbstractProxy):
    """
    TODO: a Stack that loads nested, prefixed filesystems.

        Composite(
            OSPassthrough(DIR1),
            DIR2_:OSStack(DIR2a:DIR2b),
            DIR3_:Composite(OSPassthrough(DIR3),OSStack(DIR4a:DIR4b)))

    """
    def __init__(self, prefixes):
        self.trie = datrie.Trie('0123456789abcdefghijklmnopqrstuvwxyz-:./')
        for prefix, sub in prefixes.items():
            #sub.base = prefix
            self.trie[unicode(prefix)] = Transpose(sub, '', prefix)

    def real_path(self, partial):
        pass

    def _handle(self, partial, one=False, retPref=False):
        if partial.startswith("/"):
            partial = partial[1:]
        while partial not in self.trie:
            assert partial
            partial = partial[:-1]
        k = self.trie.keys(partial)
        if one and partial:
            assert len(k) == 1
            if retPref:
                return k, self.trie[k]
            else:
                return self.trie[k]
        else:
            if retPref:
                return None, k
            else:
                return k

    def access(self, path, mode): pass
    def getattr(self, path, fh=None): pass
    def readdir(self, path, fh):
        p, fs = self._handle(path, True, True)
        yield fs

    def readlink(self, path): pass
    def statfs(self, path): pass



