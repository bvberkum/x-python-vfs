load  helper

@test "filesystem handles stat" {

  run stat $_MP/ReadMe.rst
  test_ok_nonempty || stdfail 
}

@test "filesystem handles touch existing/new/remove" {

  run touch $_MP/ReadMe.rst
  test_ok_empty || stdfail touch-existing

  TODO "touch/mkdir is not handles (bad address)"

#  run touch $_MP/New.txt
#  test_ok_empty || stdfail touch-new
#
#  run rm $_MP/New.txt
#  test_ok_empty || stdfail rm
}

#@test "filesystem handles mkdir" {
#
#  run mkdir $_MP/newDir
#  test_ok_empty || stdfail mkdir
#
#  run touch $_MP/newDir/New.txt
#  test_ok_empty || stdfail touch
#
#  run rm -rf $_MP/newDir
#  test_ok_empty || stdfail rm-rf
#}

#@test "filesystem handles 100M file" {
#
#  tmpf=./100M.bin
#  dd if=/dev/zero of=$tmpf bs=100k count=1k && sync
#  du -hs $tmpf
#  sha1=$(sha1sum $_MP/$tmpf | cut -f1 -d' ')
#  sha1_exp=$(sha1sum $tmpf | cut -f1 -d' ')
#  test "$sha1" = "$sha1_exp"
#  rm -rf $tmpf
#}

# FIXME: rsync exposed failure
#@test "filesystem handles rsync" {
#
#  mkdir src2
#  rsync -avzui src/ $_MP/src2
#  diff -bqr src $_MP/src2
#  rm -rf src2
#}
