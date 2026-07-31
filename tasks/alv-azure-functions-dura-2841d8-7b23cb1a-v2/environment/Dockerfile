FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/Azure/azure-functions-durable-js.git && git fetch --depth=1 origin 7b23cb1a17f3ee6d421b8cb5c239f80ecb587a54 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/v3.x HEAD && test "$(git rev-parse HEAD)" = 7b23cb1a17f3ee6d421b8cb5c239f80ecb587a54 && test "$(git rev-parse HEAD^{tree})" = 55c18e70586c49250bff0265c89730590c7be089
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
