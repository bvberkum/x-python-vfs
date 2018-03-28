import os
import errno

from fuse import FuseOSError

from ..ops import MyAbstractOperations
from .passthrough import OSPassthrough


class OSStack(OSPassthrough):

    """
    Stack combines as many directories as given into one, using the first
    existing path. Making it 'shadow' and potentially diverging the trees upon
    making changes.

    For example padding $PATH as argument would give a list (tree) of all
    binaries on the executable path for the shell env. Including non-executables
    and directories.
    """

    def __init__(self, paths):
        self.paths = paths.split(':')

    @property
    def args(self):
        return [str(len(self.paths))]


    # Helpers
    # =======

    def _path(self, partial, new=False, join=True):
        """
        Return base
        """
        if partial in ('', '/'): # Pick first dir
            path = p = self.paths[0]
        else:
            if partial.startswith("/"):
                partial = partial[1:]
            for p in self.paths:
                path = os.path.join(p, partial)
                if new:
                    break
                if os.path.exists(path) or os.path.islink(path):
                    break
        if not new and not os.path.exists(path) and not os.path.islink(path):
            raise FuseOSError(errno.EBADF)
        if join:
            return p
        else:
            return p, path

    def _real_path(self, partial, new=False):
        p, path = self._path(partial, new, False)
        return path

    def readdir(self, path, fh):
        dirents = ['.', '..']
        if path.startswith("/"):
            path = path[1:]
        for p in self.paths:
            real_path = os.path.join(p, path)
            if os.path.isdir(real_path):
                dirents.extend(os.listdir(real_path))
        for r in set(dirents):
            yield r

    def readlink(self, path):
        p, path = self._path(path, False, False)
        pathname = os.readlink(path)
        if not pathname.startswith("/"):
            basedir = os.path.dirname(path)
            return os.path.normpath(os.path.join(basedir, pathname))
        else:
            return pathname
