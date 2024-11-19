#!/bin/bash

THIS_DIR=$(cd $(dirname $0); pwd)
ROOT_DIR=$(cd $THIS_DIR/..; pwd)

ALL_PYCACHE_DIRS=$(find $ROOT_DIR -type d -name "__pycache__")

for _ in $ALL_PYCACHE_DIRS; do
    echo "Removing $_"
    rm -rf $_
done
