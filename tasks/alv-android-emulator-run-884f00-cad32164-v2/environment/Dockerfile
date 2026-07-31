FROM docker.io/library/node:24
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/ReactiveCircus/android-emulator-runner.git && git fetch --depth=1 origin cad321644df6d8cf1985a42767272ff068adb9cb && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = cad321644df6d8cf1985a42767272ff068adb9cb && test "$(git rev-parse HEAD^{tree})" = cf969939b0003387d367130f5322034142db9e0a
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
