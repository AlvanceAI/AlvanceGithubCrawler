FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/reyesoft/ngx-jsonapi.git && git fetch --depth=1 origin 07e0d3b97e963534bd0e129a9d758cb71f44ec92 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/2.x HEAD && test "$(git rev-parse HEAD)" = 07e0d3b97e963534bd0e129a9d758cb71f44ec92 && test "$(git rev-parse HEAD^{tree})" = c313821e8bca2e693d1e97cc1e256b3ec1bd5c5b
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
