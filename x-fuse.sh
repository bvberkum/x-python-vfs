#!/bin/sh
set -xe

mkdir -vp ./x-fuse
python x-fuse.py ./x-fuse/ "Passthrough('test')"
#python x-fuse.py ./x-fuse/ "Stack('$PATH')"
#python x-fuse.py ./x-fuse/ "Composite({'bin':Stack('$PATH')})"
