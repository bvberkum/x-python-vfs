Found little to no practical implementations, while there ought to be many.

Guess most software has little patience for those legacy non-HTTP bags of
bytes on your local harddrive. Security, performance, reliability may all
contribute to wanting to avoid custom/python based file system?

After some examples for python-fuse these where fairly simple to write:

- `OSPassthrough`, a mirror vfs of another local dir.
- `OSStack`, a mirror of several local dirs into one.
- `HideBrokenSymlinks`, like it says.

These seem to work OK, but no write test of any sort is done yet. Also while
various service-based virtual filesystems can be thought of, my initial use
cases revolve around creating composite, mirrored file trees. Read-only.

This creates a challenge to implement this in code, rather than stack an
endless mounts. If possible and ultimately desired, should want to try
to implement various composite types.

But first need to implement a transposing paths filesystem, test that.
Then continue to types that accept instances, as well as paths.

A single transpose makes not much sense. Instead the transpose type should
accept a configuration with multiple lines::

  transpose basedir to  # Translate prefix match

Then derive another type to merge with other filesystems? ::

  resolve-symlinks [pattern]

  hide pattern # Hide paths
  hide-entries pattern # Hide from dir entries list but not other access

  hide-empty-dirs [pattern]
  hide-empty-files [pattern]
  hide-broken-symlinks [pattern]


Wanted:

- `Transpose`, transform/add/remove prefixes
- `Composite`, build a tree of other vfs, map prefixes

Other ideas:

- `Hide`, hide broken symlinks, empty dirs, files or on other attributes
- `SQL/View`, format/update a record
- `JSONAsis`, read attrs from a JSONfile, like CouchDB forges JSON from dirs/files
- `JSONTree`, persist filesystem in a JSON

  - would need an outline schema
  - may like to include other vfs types, ie. make a JSONComposite
