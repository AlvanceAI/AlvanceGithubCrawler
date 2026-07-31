# Harbor rebuildable envelope v2
# Dockerfile recipe v3
# E2B aliases are optional caches; this file is the durable build source.
FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/Ovyerus/prismaliser.git && git fetch --depth=1 origin b08a906e6c19738900c7b3b0c699b249b456d07e && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = b08a906e6c19738900c7b3b0c699b249b456d07e && test "$(git rev-parse HEAD^{tree})" = 6fb2ff77af44c4e8bab3c03c23b19a338389a5da
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --immutable
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
