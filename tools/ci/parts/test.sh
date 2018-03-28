#!/bin/sh
set -e

export _MP=/tmp/x-fuse
mkdir -vp $_MP


echo '------------------------------------------------ OSPassthrough'

bats test/_not_mounted.bats

X_FUSE_BACKGROUND=false \
python x-fuse.py $_MP/ "OSPassthrough('$PWD')" &

sleep 1

bats test/_mounted.bats

bats test/os-passthrough-fs.bats
bats test/os-common.bats

${pref}umount $_MP

echo '------------------------------------------------ OSStack'

X_FUSE_BACKGROUND=false \
python x-fuse.py $_MP/ "OSStack('$PWD/:/usr/local/bin')" &

sleep 1

bats test/os-stack-fs.bats
skip="mkdir cp scp rsync" \
bats test/os-common.bats

${pref}umount $_MP

echo '------------------------------------------------ HideBrokenSymlinks'

X_FUSE_BACKGROUND=false \
python x-fuse.py $_MP/ "HideBrokenSymlinks('$PWD')" &

sleep 1

bats test/os-hide-brokensymlinks-fs.bats
bats test/os-common.bats

${pref}umount $_MP
