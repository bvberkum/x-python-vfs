@test "OSStack is mounted" {
  mount | grep OSStack
}

@test "local paths are same as OSStack mirrored paths" {

  # OSStack has merged paths from other basedir(s)
  for bin in tree curl vim wget lynx
  do
    test -e /usr/local/bin/$bin || continue
    diff -bqr $_MP/$bin /usr/local/bin/$bin || {
      echo "Failed at $bin"
    }
  done

  # File and dir look the same (to diff)
  diff -bqr $_MP/ReadMe.rst ReadMe.rst
  diff -bqr $_MP/.git .git

  # Symlink exists
  test -e $_MP/test/var/symlinks/foo

  # Broken symlink exists
  test -h $_MP/test/var/broken-symlinks/bar
}
