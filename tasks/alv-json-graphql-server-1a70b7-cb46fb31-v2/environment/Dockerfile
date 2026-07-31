FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/marmelab/json-graphql-server.git && git fetch --depth=1 origin cb46fb31256a2c72ee5a495c000ad817c1e25885 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = cb46fb31256a2c72ee5a495c000ad817c1e25885 && test "$(git rev-parse HEAD^{tree})" = 7a773d6b7c41a96925d1c4f6255006f2c83ec490
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
