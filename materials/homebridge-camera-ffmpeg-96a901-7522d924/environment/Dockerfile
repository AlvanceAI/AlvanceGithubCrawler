FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/homebridge-plugins/homebridge-camera-ffmpeg.git && git fetch --depth=1 origin 7522d924bedf922b3a7a4d71d35eb722dd3d790e && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/latest HEAD && test "$(git rev-parse HEAD)" = 7522d924bedf922b3a7a4d71d35eb722dd3d790e && test "$(git rev-parse HEAD^{tree})" = ce193ee7be4218523c4346e7dc9bc2341b70eba3
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
