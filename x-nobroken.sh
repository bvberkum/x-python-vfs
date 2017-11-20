#!/bin/sh
set -xe
mkdir -vp ./mnt/hide-broken-symlinks
#python x-fuse.py ./mnt/hide-broken-symlinks/ "HideBrokenSymlinks('test/broken-symlinks')"
#python x-fuse.py ./mnt/photos/ "Hide('/Volumes/Zephyr/Annex/photos')" &
X_FUSE_BACKGROUND=false \
  python x-fuse.py ./mnt/Kicad-mpe/ "Hide('/Volumes/Zephyr/Annex/Kicad-mpe')"
