#!/bin/sh
##MIT LICENSE applies to deb packages and to this script. for Intel media sdk 2017r3 be sure to read intel related licenses
echo "MIT LICENSE applies to deb packages and to this script. for Intel media sdk 2017r3 be sure to read intel related licenses";
echo "Using these ubuntu/debian packages is your own responsibility";
echo "Please read README.md and txt files at https://github.com/gfvh/sdk2017r3-ubuntu";
echo "Unofficial ubuntu (tested with 14_04) qsv intel media sdk 2017r3 deb packages. kernel4.4 (patched sdk 2017R3), libs, firmw, intel-sdk 2017R3(libva,libdrm,mfx,pkgconfig,opencl), grub configs, ffmpeg qsv patched";
echo "Install packages linux-image-4.4.0qsv-patch-new_4.4.0qsv-patch-new-1_amd64.deb linux-headers-4.4.0qsv-patch-new_4.4.0qsv-patch-new-1_amd64.deb h-unoff-confs-2017R3_3598.deb intel-sdk-unoff-2017R3_3598.deb ffmpeq-qsv-2017R3_3598.deb intel-gpu-top-2017R3-1-20_3598.deb";
read -p "Continue (y/n)?" CONT
if [ "$CONT" = "y" ]; then
apt-get update; apt-get -y upgrade; apt-get -y install libextutils-pkgconfig-perl libunwind8-dev libprocps3-dev libmp3lame-dev libasound2-dev libpciaccess0 libx11-dev libxext-dev libxfixes-dev libpciaccess-dev git;
cd /tmp; git clone https://github.com/gfvh/sdk2017r3-ubuntu; cd sdk2017r3-ubuntu;
dpkg -i linux-image-4.4.0qsv-patch-new_4.4.0qsv-patch-new-1_amd64.deb linux-headers-4.4.0qsv-patch-new_4.4.0qsv-patch-new-1_amd64.deb h-unoff-confs-2017R3_3598.deb intel-sdk-unoff-2017R3_3598.deb ffmpeq-qsv-2017R3_3598.deb intel-gpu-top-2017R3-1-20_3598.deb;update-grub;ldconfig
else
  echo "no";
fi
echo "rebooting now";
read -p "Continue (y/n)?" CONT
if [ "$CONT" = "y" ]; then
reboot
else
  echo "no";
fi
