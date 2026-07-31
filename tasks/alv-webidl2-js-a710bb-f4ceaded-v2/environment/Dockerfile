FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/w3c/webidl2.js.git && git fetch --depth=1 origin f4ceaded4739406321c219bfe889475071b4e34e && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = f4ceaded4739406321c219bfe889475071b4e34e && test "$(git rev-parse HEAD^{tree})" = 2ae0fc6c8e5b325c85717f395ff3eff25be8f14f
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
