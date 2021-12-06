#!/bin/bash

set -ex

pip install -r requirements/build.txt

if command -v yum &> /dev/null
then
    yum -y install \
        epel-release \
        pkgconfig \
        git \
        gcc \
        gcc-c++ \
        cmake3 \
        qt5-qtbase-devel \
        python \
        python-devel \
        python-pip \
        cmake \
        python-devel \
        python34-numpy \
        gtk2-devel \
        libpng-devel \
        jasper-devel \
        openexr-devel \
        libwebp-devel \
        libjpeg-turbo-devel \
        libtiff-devel \
        libdc1394-devel \
        tbb-devel \
        numpy \
        eigen3-devel \
        gstreamer-plugins-base-devel \
        freeglut-devel \
        mesa-libGL \
        mesa-libGL-devel \
        boost \
        boost-thread \
        boost-devel \
        libv4l-devel \
        libgomp

    cd /tmp
    git clone https://github.com/opencv/opencv.git
    git clone https://github.com/opencv/opencv_contrib.git

    cd /tmp/opencv
    mkdir build
    cd build

    cmake3 -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr/local \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D OPENCV_GENERATE_PKGCONFIG=ON \
        -D OPENCV_ENABLE_NONFREE=ON \
        -D OPENCV_EXTRA_MODULES_PATH=/tmp/opencv_contrib/modules \
        -D BUILD_EXAMPLES=OFF ..

    make -j9

    make install

    ln -s /usr/local/lib64/pkgconfig/opencv4.pc /usr/share/pkgconfig/
    ldconfig

else
    apt-get install -y \
        pkg-config \
        libeigen3-dev \
        libopencv-dev \
        libomp-dev
fi
