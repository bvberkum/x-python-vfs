#!/bin/sh
set -e

export _MP=/tmp/x-fuse
mkdir -vp $_MP
test -n "$sudo" || pref="sudo "


bats test/_not_mounted.bats

X_FUSE_BACKGROUND=false \
python x-fuse.py $_MP/ "OSPassthrough('$PWD')" &

sleep 1

bats test/_mounted.bats

bats test/os-passthrough-fs.bats
bats test/os-common.bats

${pref}umount $_MP


X_FUSE_BACKGROUND=false \
python x-fuse.py $_MP/ "OSStack('/usr/local/bin:$PWD/')" &

sleep 1

bats test/os-stack-fs.bats
bats test/os-common.bats

${pref}umount $_MP


X_FUSE_BACKGROUND=false \
python x-fuse.py $_MP/ "HideBrokenSymlinks('$PWD')" &

sleep 1

bats test/os-hide-brokensymlinks-fs.bats
bats test/os-common.bats

${pref}umount $_MP
