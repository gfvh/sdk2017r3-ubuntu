!! When using this - its your own responsibility

Unofficial ubuntu (tested with 14_04) qsv intel media sdk deb packages
Has kernel (patched sdk 2017R3), libs, firmw, intel-sdk 2017R3(libva,libdrm,mfx,pkgconfig,opencl), grub configs, ffmpeg qsv patched

Pre-Depends upon packages:

aptitude install 

libextutils-pkgconfig-perl libunwind8-dev libprocps3-dev libmp3lame-dev libasound2-dev libpciaccess0 libx11-dev libxext-dev libxfixes-dev libpciaccess-dev 

!! Works only with skylake cpu/gpu gen

After adding package run update-grub and ldconfig. after kernel update reboot.

! Add pkg h-unoff-confs-2017R3_3598.deb as last one and reboot after kernel update

!! When using this - its your own responsibility

testings:

ffmpeg 

-init_hw_device qsv:hw -y -i test.mp4 -vcodec h264_qsv -acodec copy -b:v 2M out.mp4
