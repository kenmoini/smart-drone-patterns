#!/bin/bash

# Make sure to disable nouveau driver
# https://kenmoini.com/post/2021/03/disabling-nouveau-drivers-rhel-8/

dnf groupinstall -y "Server with GUI" "base-x" "Legacy X Window System Compatibility" "Development Tools"
dnf install -y elfutils-libelf-devel gcc make kernel-headers kernel-devel acpid libglvnd-glx libglvnd-opengl libglvnd-devel pkgconfig kmod

systemctl set-default multi-user.target
systemctl isolate multi-user.target

wget https://us.download.nvidia.com/XFree86/aarch64/535.113.01/NVIDIA-Linux-aarch64-535.113.01.run

chmod a+x NVIDIA-Linux-aarch64-535.113.01.run
