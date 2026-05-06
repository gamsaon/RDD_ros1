#!/bin/bash

echo ""
echo "This script copies a udev rules to /etc/udev/rules.d/"
echo ""

#RS232
KERNELS=="3-2:1.0", SUBSYSTEMS=="usb", ATTRS{interface}=="Dual RS232-HS", SYMLINK+="RS232_MSB_Comm"
KERNELS=="3-2:1.1", SUBSYSTEMS=="usb", ATTRS{interface}=="Dual RS232-HS", SYMLINK+="RS232_MSB_Download"

#RS485
KERNELS=="3-3:1.0", SUBSYSTEMS=="usb", ATTRS{interface}=="Dual RS232-HS", SYMLINK+="RS485_MD"
KERNELS=="3-3:1.1", SUBSYSTEMS=="usb", ATTRS{interface}=="Dual RS232-HS", SYMLINK+="RS485_None"

#USB Hub
#KERNELS=="3-7.1:1.0", SUBSYSTEMS=="usb", DRIVERS=="ftdi_sio", SYMLINK+="USB_IMU"
#KERNELS=="3-7.2:1.0", SUBSYSTEMS=="usb", DRIVERS=="cp210x", SYMLINK+="USB_Lidar"
# IMU
KERNEL=="ttyUSB*", SUBSYSTEMS=="usb", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6015", ATTRS{serial}=="DP05B2UV", MODE="0777", SYMLINK+="USB_IMU", RUN+="/usr/bin/logger 'IMU rule applied'"

# Ydlidar
KERNEL=="ttyUSB*", SUBSYSTEMS=="usb", ATTRS{idVendor}=="10c4", ATTRS{idProduct}=="ea60", ATTRS{serial}=="0001", MODE="0777", SYMLINK+="USB_Lidar", RUN+="/usr/bin/logger 'Ydlidar rule applied'"

echo ""
echo "Reload udev rules"

sudo service udev reload
sudo service udev restart

echo "Set udev finish"