#!/usr/bin/env python

from __future__ import with_statement

import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations


class Passthrough(Operations):

    """
    Passthrough is a standalone filesystem class that simply 'proxies' the
    operations from one root (where the fs is mounted), to another root given as
    arguments. Iow. it mirrors a directory. But also provides for a base class
    to work on fs paths using a lookup function, called `_real_path`, so that
    subclasses can implement other mappings purely based on path name.
    """

    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _real_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        real_path = self._real_path(path)
        if not os.access(real_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        real_path = self._real_path(path)
        return os.chmod(real_path, mode)

    def chown(self, path, uid, gid):
        real_path = self._real_path(path)
        return os.chown(real_path, uid, gid)

    def getattr(self, path, fh=None):
        real_path = self._real_path(path)
        st = os.lstat(real_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                     'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size', 'st_uid'))

    def listxattr(self, path): pass
    def getxattr(self, path, name, value):
        raise FuseOSError(errno.ENOSYS)

    def readdir(self, path, fh):
        real_path = self._real_path(path)
        dirents = self.get_dirents(real_path)
        for r in dirents:
            yield r

    def get_dirents(self, real_path):
        dirents = ['.', '..']
        if os.path.isdir(real_path):
            dirents.extend(os.listdir(real_path))
        return dirents

    def readlink(self, path):
        pathname = os.readlink(self._real_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        return os.mknod(self._real_path(path, True), mode, dev)

    def rmdir(self, path):
        real_path = self._real_path(path)
        return os.rmdir(real_path)

    def mkdir(self, path, mode):
        return os.mkdir(self._real_path(path, True), mode)

    def statfs(self, path):
        real_path = self._real_path(path)
        stv = os.statvfs(real_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
            'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
            'f_frsize', 'f_namemax'))

    def unlink(self, path):
        return os.unlink(self._real_path(path))

    def symlink(self, name, target):
        return os.symlink(name, self._real_path(target))

    def rename(self, old, new):
        return os.rename(self._real_path(old), self._real_path(new, True))

    def link(self, target, name):
        return os.link(self._real_path(target), self._real_path(name, True))

    def utimens(self, path, times=None):
        return os.utime(self._real_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        real_path = self._real_path(path)
        return os.open(real_path, flags)

    def create(self, path, mode, fi=None):
        real_path = self._real_path(path)
        return os.open(real_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        real_path = self._real_path(path)
        with open(real_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        return os.fsync(fh)

    def release(self, path, fh):
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        real_path = self._real_path(path)
        return self.flush(real_path, fh)



class Stack(Passthrough):

    """
    Stack combines as many directories as given into one, using the first
    existing path. Making it 'shadow' and potentially diverging the trees upon
    making changes.

    For example padding $PATH as argument would give a list (tree) of all
    binaries on the executable path for the shell env. Including non-executables
    and directories.
    """

    def __init__(self, paths):
        self.paths = paths

    # Helpers
    # =======

    def _path(self, partial, new=False, join=True):
        if partial.startswith("/"):
            partial = partial[1:]
        for p in self.paths:
            path = os.path.join(p, partial)
            if new:
                break
            if os.path.exists(path):
                break
        if not new and not os.path.exists(path):
            raise FuseOSError(errno.EBADF)
        if join:
            return p
        else:
            return p, path

    def _real_path(self, partial, new=False):
        p, path = self._path(partial, new, False)
        return path

    def readdir(self, path, fh):
        if path.startswith("/"):
            path = path[1:]
        dirents = ['.', '..']
        for p in self.paths:
            real_path = os.path.join(p, path)
            if os.path.isdir(real_path):
                dirents.extend(os.listdir(real_path))
        for r in set(dirents):
            yield r

    def readlink(self, path):
        p, path = self._path(path, False, False)
        pathname = os.readlink(path)
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, path)
        else:
            return pathname


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
            Passthrough(DIR1),
            DIR2_:Stack(DIR2a:DIR2b),
            DIR3_:Composite(Passthrough(DIR3),Stack(DIR4a:DIR4b)))

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


class HideBrokenSymlinks(Passthrough):

    def get_dirents(self, real_path):

        """
        Hide symlinks w.o. existing target.
        """
        dirents = ['.', '..']
        if os.path.isdir(real_path):
            entries = []
            for e in os.listdir(real_path):
                p = os.path.join(real_path, e)
                if not os.path.islink(p) or os.path.exists(p):
                    entries.append(e)
            dirents.extend( entries )
        return dirents


class ResolveSymlinks(HideBrokenSymlinks):

    """
    TODO: In addition to HideBrokenSymlinks, hide all symlinks by resolve to
    real path. Read-only; should no try to update target descriptor.
    """

#    def _real_path(self, partial):
#        if partial.startswith("/"):
#            partial = partial[1:]
#        newp = os.path.realpath(os.path.abspath(os.path.join(self.root, partial)))
#        return newp


class HideSymlinksAndEmptyFolders(Passthrough):

    def scan_empty(self, real_path, entries=None):
        entries = os.listdir(real_path)
        for e in entries:
            print('scan_empty', real_path, e)
            p = os.path.join(real_path, e)
            if os.path.isdir(p):
                if self.scan_empty(p):
                    continue
                return False
            #if hide-broken-symlinks
            if os.path.islink(p) and not os.path.exists(p):
                continue
            return False
        print('empty', real_path)
        return True

    def get_dirents(self, real_path):

        """
        Hide directory entries with nothing but directories beneath.
        """

        dirents = []
        if os.path.isdir(real_path):
            entries = os.listdir(real_path)
            print(1)
            if self.scan_empty(real_path, entries):
                print(2)
                print('scan_empty', real_path)
                return ['.', '..']
            print(3)
            r = []
            for e in entries:
                p = os.path.join(real_path, e)
                if os.path.islink(p) and not os.path.exists(p):
                    continue
                r.append(e)
            dirents.extend( r )
        return ['.', '..'] + dirents


class HidePattern(Passthrough): pass

class Hide(HideSymlinksAndEmptyFolders): pass


def parse_bool(bstr):
    return bstr.lower() == 'true'

def main(mountpoint, spec):
    fuse_kwds = dict(
            nothreads=not parse_bool(os.getenv('X_FUSE_THREADS', 'false')),
            foreground=not parse_bool(os.getenv('X_FUSE_BACKGROUND', 'true'))
        )
    fs = eval(spec)
    FUSE(fs, mountpoint, **fuse_kwds)


if __name__ == '__main__':
    main(*sys.argv[1:])

#
