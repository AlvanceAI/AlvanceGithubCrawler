FROM docker.io/library/node:24
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/epam/ai-dial-chat.git && git fetch --depth=1 origin 3c6441318ebe95991d0cbc3965de039df3cc8777 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/development HEAD && test "$(git rev-parse HEAD)" = 3c6441318ebe95991d0cbc3965de039df3cc8777 && test "$(git rev-parse HEAD^{tree})" = 6e9f6fff218b1a0630669c5749f7b573ba0eadd3
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
