FROM docker.io/library/node:20
USER root
ENV HOME="/root"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/node --version && /usr/local/bin/npm --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/iamkun/dayjs.git && git fetch --depth=1 origin 98364bcebc047529345cc8c2bbcc44a6a8c18e79 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/dev HEAD && test "$(git rev-parse HEAD)" = 98364bcebc047529345cc8c2bbcc44a6a8c18e79 && test "$(git rev-parse HEAD^{tree})" = 7eac5d558684ae7339d321abe2d15fdeb43ec1d2
WORKDIR /app
RUN /usr/local/bin/npm ci
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
