@test "OSPassthrough is mounted" {
  mount | grep OSPassthrough
}

@test "local dir/file are same as OSPassthrough" {

  diff -bqr /tmp/x-fuse/ReadMe.rst ReadMe.rst
  diff -bqr /tmp/x-fuse/.git .git
}
