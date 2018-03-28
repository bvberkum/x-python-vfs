@test "HideBrokenSymlinks is mounted" {
  mount | grep HideBrokenSymlinks
}

@test "local dir/file are same but no broken symlinks" {

  # Symlink exists
  test -h /tmp/x-fuse/test/var/symlinks/foo

  # Broken symlink does not exist
  test ! -h /tmp/x-fuse/test/var/broken-symlinks/foo

  # File and dir look the same (to diff)
  diff -bqr /tmp/x-fuse/ReadMe.rst ReadMe.rst
  diff -bqr /tmp/x-fuse/.git .git
}
