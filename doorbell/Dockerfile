ARG PYTHON_VERSION_MAJOR
ARG PYTHON_VERSION_MINOR
ARG PIP_VERSION

FROM balenalib/raspberrypi3-64-python:${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}

ARG PYTHON_VERSION_MAJOR
ARG PYTHON_VERSION_MINOR
ARG PIP_VERSION
ARG PYTHON_VERSION=${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}

RUN apt update

RUN install_packages \
	x11-apps \
	x11-xserver-utils \
	libmtdev-dev \
	mesa-utils \
	libsdl2-dev \
	libsdl2-image-dev \
	libsdl2-mixer-dev \
	libsdl2-ttf-dev \
	mesa-common-dev \
	git-core \
	build-essential \
	python${PYTHON_VERSION_MAJOR}-dev \
	python${PYTHON_VERSION_MAJOR}-setuptools \
	python${PYTHON_VERSION_MAJOR}-opengl \
	# # python3-rpi.gpio \
	libjpeg-dev \
	libpng-dev 
	# libbluetooth-dev \
	# libcap2-bin \
	# bluez \
	# bluez-tools \
	# libboost-python-dev \
	# libboost-thread-dev \
	# libbluetooth-dev \
	# libglib2.0-dev

	# py${PYTHON_VERSION_MAJOR}-dbus


# RUN echo 'SUBSYSTEM=="backlight",RUN+="/bin/chmod 666 /sys/class/backlight/%k/brightness /sys/class/backlight/%k/bl_power"' | sudo tee -a /etc/udev/rules.d/backlight-permissions.rules
# RUN setcap 'cap_net_raw,cap_net_admin+eip' "$(readlink -f "$(which python)")"

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app

# RUN python --version
RUN python -m pip install --upgrade \
    pip \
	setuptools \
    wheel


COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

ENV KIVY_HOME=/usr/src/app
COPY config.ini config.ini

COPY ./app /usr/src/app/
COPY start.sh ./

ENTRYPOINT ["bash", "start.sh"]
ENV DISPLAY=:0
