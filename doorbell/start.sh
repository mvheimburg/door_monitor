#!/bin/bash


while [ `ls /tmp/.X11-unix/ | wc -l` == 0 ]; 
do 
	echo "display not created yet"; 
	sleep 0.5; 
done; 

echo "display created";
DISPLAY=`ls /tmp/.X11-unix/ | sed s/X/:/`
export DISPLAY
echo "DISPLAY is set to $DISPLAY"

while ! xset -q;
do 
	echo "Waiting for xserver"
	sleep 0.5; 
done

# python /usr/src/app/main.py
# python -m uvicorn main:app --proxy-headers --host 0.0.0.0 --port 80





cd /usr/src/app
python -m main