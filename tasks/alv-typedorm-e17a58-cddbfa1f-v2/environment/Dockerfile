FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/typedorm/typedorm.git && git fetch --depth=1 origin cddbfa1fad7c664b9aa2612ccb18b85595fa840d && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/develop HEAD && test "$(git rev-parse HEAD)" = cddbfa1fad7c664b9aa2612ccb18b85595fa840d && test "$(git rev-parse HEAD^{tree})" = 3528debbc539759d65b1c5572d2d93e7993178ee
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
