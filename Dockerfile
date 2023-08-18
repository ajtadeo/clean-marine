# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.11.4

# need to set --platform for Mac M1/M2 
FROM --platform=linux/amd64 python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Install helper packages for fetching, unzipping, and installing chrome and chromedriver
RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends
    
RUN CHROMEVER=$(curl -s "https://omahaproxy.appspot.com/linux") && \
    wget -q --continue -P /usr/bin "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$CHROMEVER/linux64/chrome-linux64.zip" && \
    unzip /usr/bin/chrome-linux64.zip -d /usr/bin && \
    chmod a+x /usr/bin/chrome-linux64 && \
    rm /usr/bin/chrome-linux64.zip

# chromedriver installs with missing dependencies, so these extra dependnecies must be installed
RUN DRIVERVER=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE") && \
    wget -q --continue -P /usr/bin "http://chromedriver.storage.googleapis.com/$DRIVERVER/chromedriver_linux64.zip" && \
    unzip /usr/bin/chromedriver_linux64.zip -d /usr/bin && \
    chmod a+x /usr/bin/chromedriver && \
    rm /usr/bin/chromedriver_linux64.zip

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python manage.py runserver 0.0.0.0:8000