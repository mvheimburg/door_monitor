#!/bin/bash


# while [ `ls /tmp/.X11-unix/ | wc -l` == 0 ]; 
# do 
# 	echo "display not created yet"; 
# 	sleep 0.5; 
# done; 
# echo "display created";

# DISPLAY=`ls /tmp/.X11-unix/ | sed s/X/:/`
# export DISPLAY
# echo "DISPLAY is set to $DISPLAY"

while ! xset -q;
do 
	echo "Waiting for xserver"
	sleep 0.5; 
done

# ln -s /usr/lib/aarch64-linux-gnu/libmpv.so2  /usr/lib/aarch64-linux-gnu/libmpv.so1 
echo "Starting doorbell"
python3 -m src.doorbell.main

