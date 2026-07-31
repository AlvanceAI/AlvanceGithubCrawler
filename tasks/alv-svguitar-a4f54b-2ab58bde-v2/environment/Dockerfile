FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/omnibrain/svguitar.git && git fetch --depth=1 origin 2ab58bdeb8797e61b0ed10f2945d296bacb23c45 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = 2ab58bdeb8797e61b0ed10f2945d296bacb23c45 && test "$(git rev-parse HEAD^{tree})" = bd6671b3b676ed9164ea409500ee6cfa496147c6
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
