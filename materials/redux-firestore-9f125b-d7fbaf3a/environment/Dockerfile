FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/prescottprue/redux-firestore.git && git fetch --depth=1 origin d7fbaf3a326634443e1372f216e3969657a288ba && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = d7fbaf3a326634443e1372f216e3969657a288ba && test "$(git rev-parse HEAD^{tree})" = 3d423421f062d1e733efd5ecaa0fca7304db0c06
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --immutable
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
