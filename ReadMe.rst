Python VFS (Virtual Filesystem)
================================
:created: 2017-05-25
:updated: 2018-03-28
:license: Simplified BSD
:status:
  .. image:: http://img.shields.io/travis/bvberkum/x-python-vfs.svg
     :target: https://travis-ci.org/bvberkum/x-python-vfs
  .. image:: https://img.shields.io/github/license/bvberkum/x-python-vfs.svg
     :alt: repo license
  .. image:: https://img.shields.io/github/commit-activity/y/bvberkum/x-python-vfs.svg
     :alt: commits per year
  .. image:: https://img.shields.io/github/languages/code-size/bvberkum/x-python-vfs.svg
  .. image:: https://img.shields.io/github/repo-size/bvberkum/x-python-vfs.svg

  master:
    .. image:: https://img.shields.io/github/last-commit/bvberkum/x-python-vfs/master.svg
      :alt: last-commit on master

  dev:
    .. image:: https://img.shields.io/github/last-commit/bvberkum/x-python-vfs/dev.svg
      :alt: last-commit on dev

  test:
    .. image:: https://img.shields.io/github/last-commit/bvberkum/x-python-vfs/test.svg
      :alt: last-commit on test


This document is on the current implementation, see also intro__.

.. __: doc/main.rst

Getting Started
---------------
Examples::

  python x-fuse.py /tmp/x-fuse/ "OSPassthrough('$PWD')"
  python x-fuse.py /tmp/x-fuse "OSStack('$PATH')"
  python x-fuse.py /tmp/x-fuse "HideBrokenSymlinks('$PWD')"

Generic invocation takes a python expression to initialize filesystem::

  python x-fuse.py ./my/path/to/mount/ "<FSType>(<FSArgs>)" [ FSName [ PIDFile ]]

These environment variables are picked up to customize FUSE behaviour; defaults::

  X_FUSE_THREADS=false
  X_FUSE_BACKGROUND=true

Testing
-------
::

  make test

Issues
------
- can't test pyvfs and py9p on OSX::

    $ mount -t 9p -o ro,port=10001 127.0.0.1 /mnt/py9p-test/
    mount: exec /Library/Filesystems/9p.fs/Contents/Resources/mount_9p for
    /mnt/py9p-test: No such file or directory


- `gdrivefs` must be compiled, which it doesn't manage on my OSX/Darwin.

ToDo
------
- Add-in LoggingMixIn, see fusepy/examples.

- Build a slightly more complex OSPassthrough with path renames/filtering.
  Besides names also may want to map or filter on type (file/dir/special),
  size, access mode.

- May want to have a go with other libs: (py)vfs/objfs, py9p.
  `fusecry` seems to install cleanly also.

Further reading
---------------
Some other things to look at. At PyPi [#]_ [#]_, at GitHub [#]_.

- `gdrivefs 0.14.8`__ access Google drive
- `mockfs 1.0.2`__
- `SVFS 2.0.0`__ - Multi-purpose virtual file system inside single file
- `fusecry 0.11.2`__ - Encrypted filesystem and encryption tool based on FUSE
  and AES.
- `CouchDB-FUSE 0.2dev`__ mount and edit CouchDB attachments

.. __: https://pypi.python.org/pypi/gdrivefs
.. __: https://pypi.python.org/pypi/mockfs/1.0.2
.. __: https://pypi.python.org/pypi/SVFS/2.0.0
.. __: https://pypi.python.org/pypi/fusecry/0.11.2
.. __: https://pypi.python.org/pypi/CouchDB-FUSE/0.2dev

On a sidenode, PyFilesystem is a suite aiming to bring a universal file-like
interface regardless of the reality. [#]_ Very neat, does it mount too?



.. [#] <https://pypi.python.org/pypi?%3Aaction=search&term=vfs&submit=search>
.. [#] <https://pypi.python.org/pypi?%3Aaction=search&term=filesystem&submit=search>
.. [#] <https://github.com/topics/filesystem>
.. [#] <https://www.pyfilesystem.org/>

..
