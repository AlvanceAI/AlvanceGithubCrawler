FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/nolanlawson/emoji-picker-element.git && git fetch --depth=1 origin 5d1c8bfc21e737c03a3cb14e06b4e472e2275ff1 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = 5d1c8bfc21e737c03a3cb14e06b4e472e2275ff1 && test "$(git rev-parse HEAD^{tree})" = 6f472068d8e7d21fa5d5bdf755b86b23a3e840b9
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/pnpm install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
