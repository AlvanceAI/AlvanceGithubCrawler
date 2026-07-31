FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/vercel/styled-jsx.git && git fetch --depth=1 origin a737ac442a9d032f9f824050b23dc9b6d766657e && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = a737ac442a9d032f9f824050b23dc9b6d766657e && test "$(git rev-parse HEAD^{tree})" = 46a21cbd4776398d618f2019bd6cc6e2ff010be5
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/pnpm install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
