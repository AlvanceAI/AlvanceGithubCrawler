FROM docker.io/library/node:22
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/xivanalysis/xivanalysis.git && git fetch --depth=1 origin f90bfac9ad9984354437b83e529f5dd709346413 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/dawntrail HEAD && test "$(git rev-parse HEAD)" = f90bfac9ad9984354437b83e529f5dd709346413 && test "$(git rev-parse HEAD^{tree})" = f0e50ed0f3b02fae8a0161c7d01172299f5487d8
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/pnpm install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
