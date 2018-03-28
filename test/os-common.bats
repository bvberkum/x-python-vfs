@test "filesystem handles 100M file" {

  tmpf=./100M.bin
  dd if=/dev/zero of=$tmpf bs=100k count=1k && sync
  du -hs $tmpf
  sha1=$(sha1sum $_MP/$tmpf | cut -f1 -d' ')
  sha1_exp=$(sha1sum $tmpf | cut -f1 -d' ')
  test "$sha1" = "$sha1_exp"
  rm -rf $tmpf
}
