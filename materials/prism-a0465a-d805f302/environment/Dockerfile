FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/PrismJS/prism.git && git fetch --depth=1 origin d805f30275e279907cbad8a339a3d899fc0ea8d8 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/v2 HEAD && test "$(git rev-parse HEAD)" = d805f30275e279907cbad8a339a3d899fc0ea8d8 && test "$(git rev-parse HEAD^{tree})" = 5329cbba54447beef86146654a1126873fd232dc
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
