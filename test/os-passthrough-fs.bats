@test "OSPassthrough is mounted" {
  mount | grep OSPassthrough
}

@test "local dir/file are same as OSPassthrough" {

  diff -bqr $_MP/ReadMe.rst ReadMe.rst
  diff -bqr $_MP/.git .git
}
