FROM docker.io/library/node:22
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/jackyzha0/quartz.git && git fetch --depth=1 origin 507ad7f3d4601d83482f61930fccf1c77f42a072 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/v5 HEAD && test "$(git rev-parse HEAD)" = 507ad7f3d4601d83482f61930fccf1c77f42a072 && test "$(git rev-parse HEAD^{tree})" = 8968345edf85ad7fb6820ec6929c20cc537471c4
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
