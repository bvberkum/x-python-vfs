#!/bin/sh
set -e

bats test/_not_mounted.bats

X_FUSE_BACKGROUND=false \
python x-fuse.py /tmp/x-fuse/ "OSPassthrough('$PWD')" &

sleep 1

bats test/_mounted.bats

bats test/os-passthrough-fs.bats

umount /tmp/x-fuse


X_FUSE_BACKGROUND=false \
python x-fuse.py /tmp/x-fuse/ "OSStack('/usr/local/bin:$PWD/')" &

sleep 1

bats test/os-stack-fs.bats

umount /tmp/x-fuse


X_FUSE_BACKGROUND=false \
python x-fuse.py /tmp/x-fuse/ "HideBrokenSymlinks('$PWD')" &

sleep 1

bats test/os-hide-brokensymlinks-fs.bats

umount /tmp/x-fuse
