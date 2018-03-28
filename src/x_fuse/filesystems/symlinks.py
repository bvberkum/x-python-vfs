"""
Some specialised symlink handling OS filesystems
"""
from __future__ import with_statement, print_function
import os

from .passthrough import OSPassthrough


class HideBrokenSymlinks(OSPassthrough):

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


class ResolveSymlinks(OSPassthrough):

    """
    TODO: In addition to HideBrokenSymlinks, hide all symlinks by resolve to
    real path. Read-only; should no try to update target descriptor.
    """

#    def _real_path(self, partial):
#        if partial.startswith("/"):
#            partial = partial[1:]
#        newp = os.path.realpath(os.path.abspath(os.path.join(self.root, partial)))
#        return newp
