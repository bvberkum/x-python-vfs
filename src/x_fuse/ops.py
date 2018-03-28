from __future__ import with_statement, print_function
import os
import errno

from fuse import FuseOSError, Operations


class MyAbstractOperations(Operations):

    def set_pidfile(self, pidfile):
        self.pidfile = pidfile

    def get_default_name(self):
        args = ','.join(self.args)
        return "%s(%s)" % ( self.__class__.__name__, args )

    @property
    def args(self):
        raise NotImplemented()

    def init(self, path):
        """Argument `path` is root, maybe chdir before FUSE call to signal mount
        point to FS Ops instance
        """
        if self.pidfile:
            print(os.getpid(), file=open(self.pidfile, 'w+'))

    def __del__(self):
        os.unlink(self.pidfile)
