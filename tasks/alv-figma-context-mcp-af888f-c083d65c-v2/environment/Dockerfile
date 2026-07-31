FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/GLips/Figma-Context-MCP.git && git fetch --depth=1 origin c083d65c7e002923e7cb98f4e3bdafb105e90f6d && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = c083d65c7e002923e7cb98f4e3bdafb105e90f6d && test "$(git rev-parse HEAD^{tree})" = 0c001ca4a63d7d0c1c1c0809e46537676210e78e
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/pnpm install --frozen-lockfile
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
