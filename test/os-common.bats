load  helper

@test "filesystem handles stat" {

  run stat $_MP/ReadMe.rst
  test_ok_nonempty || stdfail 
}

@test "filesystem handles touch existing/new/remove" {

  test "$(whoami)" = "travis" && {
    TODO "scp somehow permission denied on Travis"
  }

  run touch $_MP/ReadMe.rst
  test_ok_empty || stdfail touch-existing

  run touch $_MP/New.txt
  test_ok_empty || stdfail touch-new

  run rm $_MP/New.txt
  test_ok_empty || stdfail rm
}

@test "filesystem handles mkdir" {

  run mkdir $_MP/newDir
  test_ok_empty || stdfail mkdir

  fnmatch "* mkdir *" " $skip " && {
    rm -rf $_MP/newDir
    TODO "mkdir, rsync etc. are not properly working yet"
  }

  run touch $_MP/newDir/New.txt
  test_ok_empty || stdfail touch

  run rm -rf $_MP/newDir
  test_ok_empty || stdfail rm-rf
}

@test "filesystem handles mv" {

  touch foo.bar
  run mv $_MP/foo.bar $_MP/bar.foo
  test_ok_empty || stdfail mv
  test -e bar.foo
  rm bar.foo
}

@test "filesystem handles cp" {

  fnmatch "* cp *" " $skip " &&
    TODO "copy doesn't work"
  run cp $_MP/test/helper.bash $_MP/
  test_ok_empty || stdfail cp
  rm helper.bash
}

@test "filesystem handles scp" {

  test "$(whoami)" = "travis" &&
    TODO "scp somehow failing on Travis"

  fnmatch "* scp *" " $skip " &&
    TODO "secure copy doesn't work"
  run scp $_MP/test/helper.bash $_MP/
  test_ok_empty || stdfail scp
  rm helper.bash
}

@test "filesystem handles 100M file" {

  tmpf=./100M.bin
  dd if=/dev/zero of=$tmpf bs=100k count=1k && sync
  du -hs $tmpf
  sha1=$(sha1sum $_MP/$tmpf | cut -f1 -d' ')
  sha1_exp=$(sha1sum $tmpf | cut -f1 -d' ')
  test "$sha1" = "$sha1_exp"
  rm -rf $tmpf
}

@test "filesystem handles rsync" {

  fnmatch "* rsync *" " $skip " &&
    TODO "rsync doesn't work"

  mkdir -vp src2
  rsync -avzui src/ $_MP/src2
  diff -bqr src $_MP/src2
  rm -rf src2
} 

# TODO: more mode/attr tests
