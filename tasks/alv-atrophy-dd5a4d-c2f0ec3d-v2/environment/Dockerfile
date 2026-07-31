FROM docker.io/library/node:22
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/ashutosh-rath02/atrophy.git && git fetch --depth=1 origin c2f0ec3d6afb6f88ddfc93e5b4756e357db1807e && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = c2f0ec3d6afb6f88ddfc93e5b4756e357db1807e && test "$(git rev-parse HEAD^{tree})" = b7b8a269509924cd48613e028d6159d7d33ac62c
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
