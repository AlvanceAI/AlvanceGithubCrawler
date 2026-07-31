FROM docker.io/library/node:24
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/bhj/KaraokeEternal.git && git fetch --depth=1 origin b209d4a90aee03420eed5c14d0552b56bd7f89c5 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = b209d4a90aee03420eed5c14d0552b56bd7f89c5 && test "$(git rev-parse HEAD^{tree})" = ddf112adbfc7b4d5a3fac075aa2261c74fce36ed
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
