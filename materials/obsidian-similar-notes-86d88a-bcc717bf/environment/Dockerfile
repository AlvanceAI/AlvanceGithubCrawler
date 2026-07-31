FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/joybro/obsidian-similar-notes.git && git fetch --depth=1 origin bcc717bf9de70c29aeb14abc3ba83c5bcddd4323 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = bcc717bf9de70c29aeb14abc3ba83c5bcddd4323 && test "$(git rev-parse HEAD^{tree})" = 918b0181cb77b168689e50a05a3deb566f66d144
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
