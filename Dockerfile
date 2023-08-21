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

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
ARG UID=10001
RUN adduser \
    # --disabled-password \
    # --gecos "" \
    # --home "/nonexistent" \
    # --shell "/sbin/nologin" \
    # --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Install the latest version of Chrome
# https://gist.github.com/varyonic/dea40abcf3dd891d204ef235c6e8dd79?permalink_comment_id=3160722#gistcomment-3160722
# https://net2.com/how-to-install-google-chrome-on-ubuntu-20-04/
RUN apt-get update && \
    apt-get install -y gnupg wget curl unzip --no-install-recommends

RUN wget -q --continue https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm ./google-chrome-stable_current_amd64.deb

# Install the lastest version of Chromedriver
RUN DRIVERVER=$(curl -s "https://omahaproxy.appspot.com/linux") && \
    wget -q --continue "https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$DRIVERVER/linux64/chromedriver-linux64.zip" && \
    unzip ./chromedriver-linux64.zip -d /usr/bin && \
    chmod a+x /usr/bin/chromedriver-linux64/chromedriver && \
    rm ./chromedriver-linux64.zip

# append chrome driver location to the PATH
ENV PATH="${PATH}:/usr/bin/chromedriver-linux64"

# Switch to the non-privileged user to run the application.
USER appuser

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python manage.py runserver 0.0.0.0:8000