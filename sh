#!/bin/sh
set -xe

_MP=/tmp/x-fuse

mkdir -vp $_MP
X_FUSE_BACKGROUND=false \
python x-fuse.py $_MP "Composite({'bin':OSStack('/usr/local/bin:$PWD/')})" &
sleep 1
mount | grep x-fuse
{
ls $_MP | wc -l
ls $_MP | sort -u | wc -l
ls -la $_MP/wherefrom
ls -la $_MP
} || true
ls -la $_MP >/dev/null
umount $_MP
