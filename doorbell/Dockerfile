
ARG PYTHON_VERSION_MAJOR=3
ARG PYTHON_VERSION_MINOIR=13
ARG PYTHON=${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOIR}

FROM python:$PYTHON-slim-bookworm AS builder

ARG PYTHON_VERSION_MAJOR
ARG PYTHON

RUN apt update && apt install -y --no-install-recommends \
# 	# x11-apps \
# 	# x11-xserver-utils \
# 	# mesa-utils \
# 	# mesa-common-dev \
# 	# build-essential \
# 	# wget \
# 	# curl \
	python${PYTHON_VERSION_MAJOR}-pip \
# 	# python${PYTHON_VERSION_MAJOR}-setuptools \
# 	# python${PYTHON_VERSION_MAJOR}-opengl \
	# libmpv2 \
	# libgtk-3-dev \
	# libgstreamer1.0-dev \
	# libgstreamer-plugins-base1.0-dev \
	&& rm -rf /var/lib/apt/lists/*

RUN apt install --upgrade pip \
    && pip install pdm

WORKDIR /app
COPY pyproject.toml /app/pyproject.toml
COPY pdm.lock /app/pdm.lock
COPY /src /app/src

RUN pdm sync --no-editable
RUN echo "BUILD FINISHED"



FROM python:${PYTHON}-bookworm AS final

ARG PYTHON

RUN apt update && apt install -y --no-install-recommends \
	# libmpv2 \
	mpv \
	libmpv-dev \
	libgl1-mesa-dri \
	libgl-dev \
	libgtk-3-dev \
	libgstreamer1.0-dev \
	libgstreamer-plugins-base1.0-dev \
	x11-xserver-utils  \
	&& rm -rf /var/lib/apt/lists/*

RUN ln -s /usr/lib/aarch64-linux-gnu/libmpv.so  /usr/lib/libmpv.so.1
RUN ln -s /usr/lib/aarch64-linux-gnu/libmpv.so  /usr/lib/aarch64-linux-gnu/libmpv.so1

ENV PYTHONPATH=/app/pkgs

COPY --from=builder /app/.venv/lib/python${PYTHON}/site-packages /app/pkgs
COPY --from=builder /app/.venv/bin/* /bin/
COPY --from=builder /app /app

COPY assets /app/assets
COPY start.sh /app/start.sh
WORKDIR /app

ENV PYTHONPATH=/app/pkgs