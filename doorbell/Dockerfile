ARG PYTHON_VERSION_MAJOR
ARG PYTHON_VERSION_MINOR
ARG PIP_VERSION

FROM balenalib/raspberrypi3-64-python:${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}

ARG PYTHON_VERSION_MAJOR
ARG PYTHON_VERSION_MINOR
ARG PIP_VERSION
ARG PYTHON_VERSION=$PYTHON_VERSION_MAJOR.$PYTHON_VERSION_MINOR

RUN apt update

RUN install_packages \
    # xserver-xorg-core \
	# xinit \
	x11-apps \
	x11-xserver-utils \
	libmtdev-dev \
	mesa-utils \
	libsdl2-dev \
	libsdl2-image-dev \
	libsdl2-mixer-dev \
	libsdl2-ttf-dev \
	# libgl1-mesa-dev \
	# libgles2-mesa-dev \
	mesa-common-dev \
	git-core \
	build-essential \
	python${PYTHON_VERSION_MAJOR}-dev \
	python${PYTHON_VERSION_MAJOR}-setuptools \
	python${PYTHON_VERSION_MAJOR}-opengl \
	# # python3-rpi.gpio \
	libjpeg-dev \
	libpng-dev 

# # disable lxpolkit popup warning
# RUN mv /usr/bin/lxpolkit /usr/bin/lxpolkit.bak

# RUN echo "#!/bin/bash" > /etc/X11/xinit/xserverrc \
#   && echo "" >> /etc/X11/xinit/xserverrc \
#   && echo 'exec /usr/bin/X -s 0 dpms -nocursor -nolisten tcp "$@"' >> /etc/X11/xinit/xserverrc

# RUN echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules


RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app

# RUN python --version
RUN pip install --upgrade \
    pip \
	setuptools \
    wheel


COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


RUN ls
ENV KIVY_HOME=/usr/src/app
COPY config.ini config.ini


COPY ./app /usr/src/app/

COPY start.sh ./

ENTRYPOINT ["bash", "start.sh"]
ENV DISPLAY=:0