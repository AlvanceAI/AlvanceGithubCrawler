FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/mbeps/next_discussion_platform.git && git fetch --depth=1 origin 9d0e3574f206a9576b94f3b2aa2527ab419d0390 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = 9d0e3574f206a9576b94f3b2aa2527ab419d0390 && test "$(git rev-parse HEAD^{tree})" = 62ab49581016cf376a84a424a607dbf6fa8ec86d
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
