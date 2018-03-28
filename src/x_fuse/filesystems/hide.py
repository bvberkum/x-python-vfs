"""
TODO: Some specialised OS filesystems to hide empty folders/files or based on
pattern
"""
from __future__ import with_statement, print_function
import os

from .passthrough import OSPassthrough


class HideEmptyFolders(OSPassthrough):

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
