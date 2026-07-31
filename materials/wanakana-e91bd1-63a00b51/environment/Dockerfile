FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/WaniKani/WanaKana.git && git fetch --depth=1 origin 63a00b513979ccc96b530da2f3efb677361d573c && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = 63a00b513979ccc96b530da2f3efb677361d573c && test "$(git rev-parse HEAD^{tree})" = 433b10e729107ef87d43089423445e29b4fea0b3
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
