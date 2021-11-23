#!/bin/bash

while [[ ! -e /tmp/.X11-unix/X${DISPLAY#*:} ]]
# while [[ ! xset -q ]]
do 
	echo "Waiting for xserver"
	sleep 0.5
done

python /usr/src/app/main.py