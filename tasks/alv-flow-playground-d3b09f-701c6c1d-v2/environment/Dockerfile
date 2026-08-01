FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/onflow/flow-playground.git && git fetch --depth=1 origin 701c6c1daefbac163ea54f05c8116a3777239642 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/staging HEAD && test "$(git rev-parse HEAD)" = 701c6c1daefbac163ea54f05c8116a3777239642 && test "$(git rev-parse HEAD^{tree})" = 5196e8cef9a37dcef267b083a7ddac6f643238bc
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
