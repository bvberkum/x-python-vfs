#!/usr/bin/env python
"""Usage:

  x-fuse.py ./my/path/to/mount/ "<FSType>(<FSArgs>)" [ FSName [ PIDFile ]]
"""
from __future__ import with_statement, print_function
import os
import errno

from fuse import FUSE, FuseOSError

from x_fuse.filesystems.passthrough import OSPassthrough
from x_fuse.filesystems.stack import OSStack



def parse_bool(bstr):
    return bstr.lower() == 'true'

def main(mountpoint, spec, fsname=None, pidfile=None):
    if mountpoint[-1] != '/':
        mountpoint += '/'
    # FUSE Operations instance from argv
    fs = eval(spec)
    if not pidfile:
        pidfile = "%s-fuse.pid" % os.path.abspath(mountpoint[:-1])
    fs.set_pidfile(pidfile)
    # FUSE parameters from argv/env
    if not fsname:
        fsname = fs.get_default_name()
    fuse_kwds = dict(
            fsname=fsname,
            nothreads=not parse_bool(os.getenv('X_FUSE_THREADS', 'false')),
            foreground=not parse_bool(os.getenv('X_FUSE_BACKGROUND', 'true')),
        )
    # Start as requested
    FUSE(fs, mountpoint, **fuse_kwds)


if __name__ == '__main__':
    import sys ; args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    elif '-h' in args:
        print(__doc__)
        sys.exit(0)
    main(*sys.argv[1:])
