FROM balenalib/raspberrypi4-64-debian-python:3.7.8


RUN install_packages \
	build-essential \ 
	libssl-dev \
	libffi-dev \
	python-dev

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app

RUN python --version
RUN pip install -U \
	pip \
	setuptools

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


COPY ./app /usr/src/app/


CMD ["python", "/usr/src/app/main.py"]

#####################################################################