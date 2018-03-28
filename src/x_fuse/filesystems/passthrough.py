from __future__ import with_statement, print_function
import os
import errno

from fuse import FuseOSError

import x_fuse.filesystems
from x_fuse.ops import MyAbstractOperations


class OSPassthrough(MyAbstractOperations):

    """
    Passthrough is a standalone filesystem class that simply 'proxies' the
    operations from one root (where the fs is mounted), to another root given as
    arguments. Iow. it mirrors a directory. But also provides for a base class
    to work on fs paths using a lookup function, called `_real_path`, so that
    subclasses can implement other mappings purely based on path name.
    """

    def __init__(self, root):
        self.root = root
        self.pidfile = None

    @property
    def args(self):
        return [self.root]

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
        if stv:
            d = dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
                'f_frsize', 'f_namemax'))
        else:
            d = dict((key, 0) for key in ('f_bavail', 'f_bfree',
                'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files', 'f_flag',
                'f_frsize', 'f_namemax'))
            d['f_namemax'] = 255
        return d

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

