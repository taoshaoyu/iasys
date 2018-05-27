#!/bin/bash

# cd <BUSYBOX>/_install; exec init_bb_initrd.sh

ln -s bin/busybox init
mkdir dev
mkdir sys
mkdir proc
mkdir etc
mkdir etc/init.d
mkdir var
mkdir var/run
mkdir etc/network
mkdir etc/network/if-pre-up.d
mkdir etc/network/if-up.d
mkdir run
mkdir tmp

#etc/fstab
cat > etc/fstab << EOF
none		/run		tmpfs	nosuid,size=10%,mode=755	0	0
none		/proc		proc	defaults        0	0
none		/sys		sysfs	defaults	0	0
EOF

#etc/init.d/rcS
cat > etc/init.d/rcS <<EOF
#!/bin/sh
/bin/mount -a
/bin/mount -n -o mode=0755 -t devtmpfs devtmpfs /dev
mkdir -p /dev/pts
mount -t devpts -o noexec,nosuid,gid=5,mode=0620 devpts /dev/pts
EOF
chmod +x etc/init.d/rcS

#etc/inittab
cat > etc/inittab << EOF
::sysinit:/etc/init.d/rcS
::askfirst:-/bin/sh
tty2::askfirst:-/bin/sh
tty3::askfirst:-/bin/sh
tty4::askfirst:-/bin/sh
#ttyS0::askfirst:-/bin/sh

tty4::respawn:/sbin/getty 38400 tty5
tty5::respawn:/sbin/getty 38400 tty6

::restart:/sbin/init

::ctrlaltdel:/sbin/reboot
::shutdown:/bin/umount -a -r
::shutdown:/sbin/swapoff -a
EOF

# create /lib/modules ....   skip

#etc/network/interfaces
cat > etc/network/interfaces << EOF
auto eth0
iface eth0 inet static
  address 192.168.2.10
  netmask 255.255.255.0
  gateway 192.168.2.254
EOF


