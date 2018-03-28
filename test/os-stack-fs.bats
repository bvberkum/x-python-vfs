@test "OSStack is mounted" {
  mount | grep OSStack
}

@test "local paths are same as OSStack mirrored paths" {

  # OSStack has merged paths from other basedir(s)
  for bin in tree curl vim wget lynx
  do
    test -e /usr/local/bin/$bin || continue
    diff -bqr /tmp/x-fuse/$bin /usr/local/bin/$bin || {
      echo "Failed at $bin"
    }
  done

  # File and dir look the same (to diff)
  diff -bqr /tmp/x-fuse/ReadMe.rst ReadMe.rst
  diff -bqr /tmp/x-fuse/.git .git

  # Symlink exists
  test -e /tmp/x-fuse/test/var/symlinks/foo

  # Broken symlink exists
  test -h /tmp/x-fuse/test/var/broken-symlinks/bar
}
