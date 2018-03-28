Python VFS (Virtual Filesystem)
================================
:created: 2017-05-25
:updated: 2018-03-28
:license: Simplified BSD
:status: experimental

Found little to no practical implementations, while there ought to be many.

Guess most software has little patience for those legacy non-HTTP bags of
bytes on your local harddrive. Security, performance, reliability may all
contribute to wanting to avoid custom/python based file system?

After some examples for python-fuse these where fairly simple:

- `OSPassthrough`_, a mirror vfs of another local dir.
- `OSStack`_, a mirror of several local dirs into one.

Wanted

- `Transpose`, transform/add/remove prefixes
- `Composite`, build a tree of other vfs, map prefixes

Ideas

- `Hide`, hide broken symlinks, empty dirs, files or on other attributes
- `SQL/View`, format/update a record
- `JSONAsis`, read attrs from a JSONfile, like CouchDB forges JSON from files
- `JSONTree`, persist filesystem in a JSON

  - would need an outline schema
  - may like to include other vfs types, ie. make a JSONComposite


.. _OSPassthrough: x-fuse.py
.. _OSStack: x-fuse.py

Getting Started
---------------
Examples::

  python x-fuse.py /tmp/x-fuse/ "OSPassthrough('$PWD')"
  python x-fuse.py /tmp/x-fuse "OSStack('$PATH')"

Generic invocation takes a python expression to initialize filesystem::

  python x-fuse.py ./my/path/to/mount/ "<FSType>(<FSArgs>)" [ FSName [ PIDFile ]]

These environment variables are picked up to customize FUSE behaviour; defaults::

  X_FUSE_THREADS=false
  X_FUSE_BACKGROUND=true


Issues
------
- can't test pyvfs and py9p on OSX::

    $ mount -t 9p -o ro,port=10001 127.0.0.1 /mnt/py9p-test/
    mount: exec /Library/Filesystems/9p.fs/Contents/Resources/mount_9p for
    /mnt/py9p-test: No such file or directory


- `gdrivefs` must be compiled, which it doesn't manage on my OSX/Darwin.

ToDo
------
- `fusecry` seems to install cleanly, play with that a bit.
- Split up code from x-fuse.py in some sensible manner.

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
