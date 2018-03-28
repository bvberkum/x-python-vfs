@test "OSStack is mounted" {
  mount | grep OSStack
}

@test "local dir/file are same as OSStack" {

  diff -bqr /tmp/x-fuse/ReadMe.rst ReadMe.rst
  diff -bqr /tmp/x-fuse/.git .git
  diff -bqr /tmp/x-fuse/vim /usr/local/bin/vim
}
