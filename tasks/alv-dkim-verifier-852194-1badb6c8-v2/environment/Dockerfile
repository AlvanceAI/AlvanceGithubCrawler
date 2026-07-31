FROM docker.io/library/node:26
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/lieser/dkim_verifier.git && git fetch --depth=1 origin 1badb6c8d639bd5973f870fa7bfc6f96facba9ca && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = 1badb6c8d639bd5973f870fa7bfc6f96facba9ca && test "$(git rev-parse HEAD^{tree})" = 8c48e92f6ec1cb2a5c150f929e5598a1f67eb26d
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
