FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/minop1205/react-dnd-treeview.git && git fetch --depth=1 origin d3163ab29d01a8e35d57a8da5ecf945657360189 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/next HEAD && test "$(git rev-parse HEAD)" = d3163ab29d01a8e35d57a8da5ecf945657360189 && test "$(git rev-parse HEAD^{tree})" = e17d312babb3405b14e9e41bdda90027682ceeb8
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
