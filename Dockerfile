FROM balenalib/raspberrypi4-64-debian-python:latest


# EGL work around for containers
WORKDIR /opt/vc
RUN wget https://github.com/resin-io-playground/userland/releases/download/v0.1/userland-rpi.tar.xz
RUN tar xf userland-rpi.tar.xz

WORKDIR /usr/src/app
ENV KIVY_HOME=/usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

RUN git clone https://github.com/kivy/kivy && cd kivy && python setup.py build && python setup.py install


COPY . .

CMD [ "python", "./your-daemon-or-script.py" ]