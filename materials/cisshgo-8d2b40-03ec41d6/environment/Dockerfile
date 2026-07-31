FROM docker.io/library/golang:1.22
USER root
ENV GOCACHE="/root/.cache/go-build"
ENV GOMODCACHE="/go/pkg/mod"
ENV GOPATH="/go"
ENV GOPROXY="https://goproxy.cn,direct"
ENV GOTOOLCHAIN="auto"
ENV HOME="/root"
ENV PATH="/usr/local/go/bin:/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/go/bin/go version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/tbotnz/cisshgo.git && git fetch --depth=1 origin 03ec41d603010333b25f378add32dc5a19578608 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = 03ec41d603010333b25f378add32dc5a19578608 && test "$(git rev-parse HEAD^{tree})" = 3a731a631ea7b7aba227d1e130c3442d96828cfc
WORKDIR /app
RUN /usr/local/go/bin/go mod download
RUN /usr/local/go/bin/go build ./...
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
