FROM docker.io/library/node:24
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/actions/download-artifact.git && git fetch --depth=1 origin 484a0b528fb4d7bd804637ccb632e47a0e638317 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = 484a0b528fb4d7bd804637ccb632e47a0e638317 && test "$(git rev-parse HEAD^{tree})" = 91835e479e20dd333f17e753a01f3d238fc6cf7e
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
