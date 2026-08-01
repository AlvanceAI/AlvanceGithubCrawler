FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/jupyter-widgets/ipydatagrid.git && git fetch --depth=1 origin 0685635938395866ba3f9b62bcca8fa4c973d7d7 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = 0685635938395866ba3f9b62bcca8fa4c973d7d7 && test "$(git rev-parse HEAD^{tree})" = 42fafc997cc0bada1e7bff9e959a95e037e85629
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --immutable
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
