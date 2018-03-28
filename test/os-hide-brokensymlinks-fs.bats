@test "HideBrokenSymlinks is mounted" {
  mount | grep HideBrokenSymlinks
}

@test "local dir/file are same but no broken symlinks" {

  # Symlink exists
  test -h $_MP/test/var/symlinks/foo

  # Broken symlink does not exist
  test ! -h $_MP/test/var/broken-symlinks/foo

  # File and dir look the same (to diff)
  diff -bqr $_MP/ReadMe.rst ReadMe.rst
  diff -bqr $_MP/.git .git
}
