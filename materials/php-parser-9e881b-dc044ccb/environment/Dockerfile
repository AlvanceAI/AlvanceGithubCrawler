FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/glayzzle/php-parser.git && git fetch --depth=1 origin dc044ccbe9ac00e2a88f23eee3093ae24937824a && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = dc044ccbe9ac00e2a88f23eee3093ae24937824a && test "$(git rev-parse HEAD^{tree})" = fe6ffadf69ca04ddad516da50079f8806bb734a4
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --immutable
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
