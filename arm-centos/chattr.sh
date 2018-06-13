#!/bin/bash
rpm2cpio /home/taosy/mirrors/centos.mirror.moack.net/centos-altarch/7.5.1804/os/armhfp/Packages/filesystem-3.2-25.el7.armv7hl.rpm | cpio -imdv
chmod +w bin/
chmod +w lib/
chmod +w usr/sbin/