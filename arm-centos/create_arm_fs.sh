#!/bin/bash

~/work/myproj/iasys/arm-centos/chattr.sh
~/work/myproj/iasys/ctfs.sh -s ~/mirrors/centos.mirror.moack.net/centos-altarch/7.5.1804/os/armhfp/Packages/ -l ~/work/myproj/iasys/arm-centos/f2.txt
ln -s usr/lib/systemd/systemd-bootchart init
chmod 755 usr/bin/mount
sudo groupadd -r -g 11 cdrom -R `pwd`
sudo groupadd -r -g 22 utmp  -R `pwd`
sudo groupadd -r -g 192 systemd-network -R `pwd`
#FIXME, missing -g 192 or -g systemd-network
sudo useradd  -R `pwd` -r -u 192 -l  -d / -s /sbin/nologin -c "systemd Network Management" systemd-network  
sudo groupadd -r -g 190 systemd-journal -R `pwd`
sudo groupadd -r input -R `pwd`
ln -sf ../proc/self/mounts etc/mtab
sudo useradd  -R `pwd` -m -s /bin/bash taosy

mkdir -p etc/systemd/system/serial-getty@.service.d
cat > etc/systemd/system/serial-getty@.service.d/autologin.conf.bak << EOF
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin root --noclear %I 38400 vt102
EOF

sudo groupadd -r -g 81 dbus -R `pwd`
sudo useradd -c 'System message bus' -u 81  -s /sbin/nologin -r -d '/' dbus -R `pwd`

ln -s /run/dbus/ var/run/dbus