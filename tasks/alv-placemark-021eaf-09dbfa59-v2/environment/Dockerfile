FROM docker.io/library/node:22
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/placemark/placemark.git && git fetch --depth=1 origin 09dbfa59704aa7b7f2836604d06c6fb508875c4f && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = 09dbfa59704aa7b7f2836604d06c6fb508875c4f && test "$(git rev-parse HEAD^{tree})" = 3c8d2134e1ee0e71f405a01d8a6118d55473df9e
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/pnpm install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
