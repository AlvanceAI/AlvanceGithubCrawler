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
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/rwxrob/bonzai.git && git fetch --depth=1 origin 236ed3a82d59af3318fd6674e82f0f67629ef205 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = 236ed3a82d59af3318fd6674e82f0f67629ef205 && test "$(git rev-parse HEAD^{tree})" = b8f0de349bc2dad84ed253a259d6a07c0042a42a
WORKDIR /app
RUN /usr/local/go/bin/go mod download
RUN /usr/local/go/bin/go build ./...
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
