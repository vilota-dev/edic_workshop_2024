# Workshop Plan
## What You need
1. A laptop with Ubuntu Linux, or Windows with Virtualbox Ubuntu Linux
2. To work with the example, you need a laptop with working webcam

## Part 1 - eCAL Robotics Middleware with Capnproto Serialisation (2hr)
You will code in Python and perform Apriltag detection on your webcam! At the same time, serialise the information using eCAL and capnproto to share the information to other nodes of robotics software.
1. Working with pyapriltags library and OpenCV
2. Install capnproto dependency and load the message definitions
3. Install and import eCAL middleware, learn to publish topics
4. Receive on another Python script

## Part 2 - Visualisation using Rerun.io (0.5hr)
1. Visualisation of tags and images using rerun framework
2. Optionally, record data into mcap format


## Installation

### Virtual Box Download

https://www.virtualbox.org/wiki/Downloads


#### Install Extension Pack

https://scribles.net/using-webcam-in-virtualbox-guest-os-on-windows-host/

### Ubuntu 22.04 Image

https://www.releases.ubuntu.com/22.04/

Use the desktop image



## Bring up Webcam in VirtualBox Ubuntu Client, Windows Host

https://askubuntu.com/a/894507


## Tag Detection Using Apriltag Lib and OpenCV

```
pip3 install pyapriltags
```


## Intall eCAL

```
sudo add-apt-repository ppa:ecal/ecal-5.12
sudo apt-get update
sudo apt-get install ecal

sudo apt install python3-ecal5
```
