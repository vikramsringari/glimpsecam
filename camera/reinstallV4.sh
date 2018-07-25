#!/bin/bash
echo "******************************"
echo "* GlimpseCam Setup Script    *"
echo "* Developed by Tianhao Zhang *"
echo "* Copyright (C) 2018         *"
echo "******************************"
echo ""
echo "NOTE:"
echo "PLEASE PUT THIS SCRIPT INTO HOME DIRECTORY"
echo ""

if [ $# -eq 0 ]; then
	echo "Which Module(s) Would You Like to Install?"
	echo "(1) Update to Latest Raspbian"
	echo "(2) Install Pikrellcam Library"
	echo "(3) Install AWS CLI"
	echo "(4) Personalization"	
	echo "(5) Install Dropbox Uploader"
	echo "(6) Install ALL but Dropbox Uploader"
	echo "(7) Install ALL"
	read -p "Please Enter Your Selection (1-7): " ANSWER
else
	ANSWER=$1
fi

if [[ $ANSWER != [1-7] ]]; then
	echo "INVALID SELECTION!"
	exit 1
fi

# Update to Latest Version Raspbian
if [ $ANSWER -eq 1 -o $ANSWER -eq 6 -o $ANSWER -eq 7 ]; then
	echo ""
	echo "-----------------------------"
	echo "UPDATE TO LATEST RASPBIAN"
	echo "-----------------------------"
	echo ""
	sudo apt-get install
	sudo apt-get update
fi

# Install Pikrellcam library
if [ $ANSWER -eq 2 -o $ANSWER -eq 6 -o $ANSWER -eq 7 ]; then
	echo ""
	echo "-----------------------------"
	echo "INSTALL PIKRELLCAM LIBRARY"
	echo "-----------------------------"
	echo ""
	cd /home/pi
	git clone https://github.com/billw2/pikrellcam
	cd pikrellcam
	chmod u+rwx install-pikrellcam.sh
	./install-pikrellcam.sh
fi

# Install AWS CLI
if [ $ANSWER -eq 3 -o $ANSWER -eq 6 -o $ANSWER -eq 7 ]; then
	echo ""
	echo "-----------------------------"
	echo "INSTALL AWS CLI"
	echo "-----------------------------"
	echo ""
	cd /home/pi
	curl "https://s3.amazonaws.com/aws-cli/awscli-bundle.zip" -o "awscli-bundle.zip"
	unzip awscli-bundle.zip
	sudo ./awscli-bundle/install -i /usr/local/aws -b /usr/local/bin/aws
	aws configure
fi

# Personalization
if [ $ANSWER -eq 4 -o $ANSWER -eq 6 -o $ANSWER -eq 7 ]; then
	echo ""
	echo "-----------------------------"
	echo "Please Set Up the TimeZone Information."
	echo "-----------------------------"
	sleep 3
	sudo dpkg-reconfigure tzdata
	echo "-----------------------------"
	echo "Please Change the Default Password and "
	echo "Enable the Camera, SSH, and VNC through Interface Options."
	echo "-----------------------------"
	sleep 3
	sudo raspi-config
	echo ""
fi

# Install Dropbox Uploader
if [ $ANSWER -eq 5 -o $ANSWER -eq 7 ]; then
	echo "-----------------------------"
	echo "Install Dropbox"
	echo "-----------------------------"
	echo ""
	cd /home/pi
	git clone https://github.com/andreafabrizi/Dropbox-Uploader.git
	cd Dropbox-Uploader
	chmod u+rwx dropbox_uploader.sh
	echo "-------"
	echo "Note:"
	echo "Access Token is 5YWMfG1RFfAAAAAAAAAAr5bEXrgq3vdg8U-nZA4b8CZOwWiwqPz2Wr7JvQ2Jyf1z"
	echo "-------"
	./dropbox_uploader.sh
fi

echo "Congradulations! The Setup is now complete!"

 
