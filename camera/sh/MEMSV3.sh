#!/bin/bash
RED='\033[0;31m'
NC='\033[0m'
echo "***********************************"
echo "* MEMS Microphone Setup Script    *"
echo "* Developed by Tianhao Zhang      *"
echo "* Copyright (C) 2018              *"
echo "***********************************"
echo ""
echo "NOTE:"
echo -e "PLEASE CLOSE ${RED}ALL ${NC}OTHER PROGRAMS."
echo -e "MAKE SURE YOU RUN THIS SCRIPT AS ${RED}SUDO ${NC}USER."
echo ""

read -p "Are you running the shell script as SUDO USER? (y/n) " ANSWER
case "$ANSWER" in 
	[yY][eE][sS]|[yY] ) echo "";;
	* ) echo "Usage: sudo ./MEMSV3.sh" 
	    exit 1
	    ;;
esac

cd /home/pi
if [ -e boot1.zth ]; then
	echo "boot1.zth Exists"
	echo "Continue Installation Process..."
	rm boot1.zth
	sudo apt-get update
	sudo apt-get install rpi-update
	sudo rpi-update
	touch boot2.zth
	echo "Rebooting in 5 Seconds!"
    sleep 5
    sudo reboot
elif [ -e boot2.zth ]; then
	echo "boot2.zth Exists"
	echo "Continue Installation Process..."
	rm boot2.zth
	sudo apt-get install git bc libncurses5-dev
	sudo wget https://raw.githubusercontent.com/notro/rpi-source/master/rpi-source -O /usr/bin/rpi-source
	sudo chmod +x /usr/bin/rpi-source
	/usr/bin/rpi-source -q --tag-update
	rpi-source --skip-gcc
	sudo mount -t debugfs debugs /sys/kernel/debug
	git clone https://github.com/PaulCreaser/rpi-i2s-audio
	cd rpi-i2s-audio	
	sed -i "s/3f203000/20203000/g" my_loader.c
	make -C /lib/modules/$(uname -r )/build M=$(pwd) modules
	sudo insmod my_loader.ko
	sudo cp my_loader.ko /lib/modules/$(uname -r)
	echo 'my_loader' | sudo tee --append /etc/modules > /dev/null
	sudo depmod -a
	sudo modprobe my_loader
	cd /home/pi
	touch boot3.zth
    echo "Rebooting in 5 Seconds!"
    sleep 5
    sudo reboot
elif [ -e boot3.zth ]; then
	echo "boot3.zth Exists"
	echo "Continue Installation Process..."
	rm boot3.zth
	wget https://raw.githubusercontent.com/vikramsringari/glimpsecam/master/camera/sh/asoundrc
	sudo cp glimpsecam/camera/sh/asoundrc ~/.asoundrc
	timeout 3 arecord -D dmic_sv -c2 -r 44100 -f S32_LE -t wav -V mono -v file.wav
	cd /home/pi
	touch complete.zth
	echo "Congratulations! The Installation of MEMS Microphone is Now Complete!"
elif [ -e complete.zth ]; then
	echo "The MEMS Microphone has already been installed!"
else
	echo ""
    echo "-----------------------------"
    echo "INSTALL MEMS Microphone"
    echo "-----------------------------"
    echo ""
	echo "Modifying /boot/config.txt..."
    sudo sed -i '/#dtparam=i2s=on/c\dtparam=i2s=on' /boot/config.txt
    echo "Modifying /etc/modules..."
    sudo echo "snd-bcm2835" >> /etc/modules
	touch boot1.zth
	echo "Rebooting in 5 Seconds!"
	sleep 5
	sudo reboot
fi
