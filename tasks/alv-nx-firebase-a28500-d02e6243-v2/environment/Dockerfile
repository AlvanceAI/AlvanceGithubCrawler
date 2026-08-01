FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/simondotm/nx-firebase.git && git fetch --depth=1 origin d02e6243cb27c8aded576338f2a33fa4b9d4fa5b && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = d02e6243cb27c8aded576338f2a33fa4b9d4fa5b && test "$(git rev-parse HEAD^{tree})" = c47b3e124391bec978790592310d72b08e8951e0
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/pnpm install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
