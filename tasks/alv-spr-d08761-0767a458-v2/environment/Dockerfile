FROM docker.io/library/golang:1.22
USER root
ENV GOCACHE="/root/.cache/go-build"
ENV GOMODCACHE="/go/pkg/mod"
ENV GOPATH="/go"
ENV GOPROXY="https://goproxy.cn,direct"
ENV GOTOOLCHAIN="local"
ENV HOME="/root"
ENV PATH="/usr/local/go/bin:/go/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/go/bin/go version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/ejoffe/spr.git && git fetch --depth=1 origin 0767a458e50fa1f7ae203b73e50298ab201c80bb && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = 0767a458e50fa1f7ae203b73e50298ab201c80bb && test "$(git rev-parse HEAD^{tree})" = 65b360b4fc47a38bcf5c4c54a25848d6ad122126
WORKDIR /app
RUN /usr/local/go/bin/go mod download
RUN /usr/local/go/bin/go build ./...
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
