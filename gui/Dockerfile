FROM balenalib/raspberrypi4-64-debian-python:3.7.8

RUN install_packages \
    xserver-xorg-video-fbdev \
    xserver-xorg xinit \
    xterm x11-xserver-utils \
    xterm \
    xserver-xorg-input-evdev \
    xserver-xorg-legacy \
    mesa-vdpau-drivers \
	pkg-config \
	cec-utils \
	lsb-release \
    libgles2-mesa \
	libsdl2-dev \
	libsdl2-image-dev \
	libsdl2-mixer-dev \
	libsdl2-ttf-dev \
	libgl1-mesa-dev \
	libgles2-mesa-dev \
	libgstreamer1.0-dev \
	git-core \
	gcc \
	python-pip \
	gstreamer1.0-plugins-base \
	gstreamer1.0-plugins-good \
	gstreamer1.0-plugins-bad \
	gstreamer1.0-plugins-ugly \
	gstreamer1.0-alsa \
	python-dev \
	python-setuptools \
	python3-rpi.gpio \
	cython \
	wget \
	xclip

# disable lxpolkit popup warning
# RUN mv /usr/bin/lxpolkit /usr/bin/lxpolkit.bak

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app

RUN python --version
RUN pip install -U \
	pip \
	setuptools


COPY prerequirements.txt ./
RUN pip install --no-cache-dir -r prerequirements.txt

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

##########################################################

# RUN pip install adafruit-circuitpython-pn532

##########################################################

# RUN apt install bzr i2c-tools libnfc5 libnfc-bin 

RUN pip install -U pyserial twine ndef nfcpy

#########################################################


# ENV UDEV=1
RUN echo "#!/bin/bash" > /etc/X11/xinit/xserverrc \
  && echo "" >> /etc/X11/xinit/xserverrc \
  && echo 'exec /usr/bin/X -s 0 dpms -nocursor -nolisten tcp "$@"' >> /etc/X11/xinit/xserverrc

# RUN echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules

RUN ls
ENV KIVY_HOME=/usr/src/app
COPY config.ini config.ini

# RUN git clone https://github.com/kivy/kivy && cd kivy && python setup.py build && python setup.py install

COPY ./app /usr/src/app/

COPY start.sh ./

CMD ["bash", "start.sh"]

#####################################################################