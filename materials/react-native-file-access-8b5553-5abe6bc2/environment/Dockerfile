FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/alpha0010/react-native-file-access.git && git fetch --depth=1 origin 5abe6bc24581a12f173f745226e4afe73e482d5d && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = 5abe6bc24581a12f173f745226e4afe73e482d5d && test "$(git rev-parse HEAD^{tree})" = b0c5a57a97a27bbe1e58bd1fcfd758a4721f6c22
WORKDIR /app
RUN /usr/local/bin/corepack enable && /usr/local/bin/yarn install --immutable
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
