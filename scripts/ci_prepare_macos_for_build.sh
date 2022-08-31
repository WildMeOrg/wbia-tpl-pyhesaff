#!/bin/bash

set -ex

pip install -r requirements/build.txt

brew install \
    pkg-config \
    eigen \
    opencv \
    libomp

python setup.py build_ext --inplace
