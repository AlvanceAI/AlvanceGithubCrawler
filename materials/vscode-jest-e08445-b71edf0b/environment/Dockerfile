FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/jest-community/vscode-jest.git && git fetch --depth=1 origin b71edf0b1b80aa22a16222775fbd37dabab3aea0 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = b71edf0b1b80aa22a16222775fbd37dabab3aea0 && test "$(git rev-parse HEAD^{tree})" = 295d5d003016714ff8fdbab4439d587e896e6366
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
