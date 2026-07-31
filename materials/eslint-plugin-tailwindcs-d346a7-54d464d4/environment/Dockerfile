FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/francoismassart/eslint-plugin-tailwindcss.git && git fetch --depth=1 origin 54d464d472775c63a1855d326fff692db92aa0b8 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/v4 HEAD && test "$(git rev-parse HEAD)" = 54d464d472775c63a1855d326fff692db92aa0b8 && test "$(git rev-parse HEAD^{tree})" = a77d563f2ba076c4a8f492a07fe0ada05d3ae35d
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/pnpm install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
