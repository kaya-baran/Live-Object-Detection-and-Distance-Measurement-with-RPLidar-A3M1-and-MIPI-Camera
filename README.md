# Live-Object-Detection-and-Distance-Measurement-with-RPLidar-and-MIPI-Camera

This project is conducted on Jetson Nano and by using RPLidar and MIPI Camera. It is a library that returns the distance of the object at the point clicked on the video output.

## Libraries and Installation

The libraries used in this project are [OpenCV](https://docs.opencv.org/master/d2/de6/tutorial_py_setup_in_ubuntu.html), [pynput](https://pypi.org/project/pynput/), [PyRPlidar](https://pypi.org/project/pyrplidar/), [argparse](https://docs.python.org/3/library/argparse.html),  [numpy](https://pypi.org/project/numpy/) and [jetson.inference and jetson.utils](https://github.com/dusty-nv/jetson-inference).
```bash
sudo apt-get install python3-opencv
pip3 install pynput
pip3 install pyrplidar
pip3 install argparse
pip3 install numpy
```
You can find how to install jetson.inference and jetson.utils [here](https://github.com/dusty-nv/jetson-inference).
I also added these configurations of OpenCV:

```bash
cmake -D WITH_CUDA=ON -D WITH_CUDNN=OFF -D CUDA_ARCH_BIN="5.3,6.2,7.2" -D CUDA_ARCH_PTX="" -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.3.0/modules -D WITH_GSTREAMER=ON -D WITH_LIBV4L=ON -D BUILD_opencv_python2=ON -D BUILD_opencv_python3=ON -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D BUILD_EXAMPLES=OFF -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..
```
