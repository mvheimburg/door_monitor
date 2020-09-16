FROM balenalib/raspberrypi4-64-debian-python:3.7.8


# install required packages
# RUN install_packages \
# 	build-essential \ 
# 	libssl-dev \
# 	libffi-dev \
# 	python-dev

RUN apt-get update && apt-get install -yq --no-install-recommends \
    bluez && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# define our working directory in the container
RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app

# copy all files in our root to the working directory
COPY . ./

# enable systemd init system in the container
# ENV INITSYSTEM on

# scan.sh will run when the container starts up on the device
CMD ["bash", "scan.sh"]