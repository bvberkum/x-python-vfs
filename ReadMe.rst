Python VFS (Virtual Filesystem)
================================
:created: 2017-05-25
:updated: 2017-05-25
:license: Simplified BSD
:status: experimental

Found little to no practical implementations, while there ought to be many.

Guess most software has little patience for those legacy non-HTTP bags of
bytes on your local harddrive. Security, performance, reliability may all
contribute to wanting to avoid python based file system?

After some examples for python-fuse these where fairly simple:

- `OSPassthrough`, a mirror vfs of another local dir.
- `OSStack`, a mirror of several local dirs into one.

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

Issues
------
- can't test pyvfs and py9p on OSX::

    $ mount -t 9p -o ro,port=10001 127.0.0.1 /mnt/py9p-test/
    mount: exec /Library/Filesystems/9p.fs/Contents/Resources/mount_9p for
    /mnt/py9p-test: No such file or directory

..
