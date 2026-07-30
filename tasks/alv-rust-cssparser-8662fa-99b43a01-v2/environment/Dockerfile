# Harbor rebuildable envelope v2
# Dockerfile recipe v3
# E2B aliases are optional caches; this file is the durable build source.
FROM docker.io/library/rust:1.71
USER root
ENV CARGO_HOME="/usr/local/cargo"
ENV HOME="/root"
ENV PATH="/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV RUSTUP_HOME="/usr/local/rustup"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/cargo/bin/rustc --version && /usr/local/cargo/bin/cargo --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/servo/rust-cssparser.git && git fetch --depth=1 origin 99b43a015d9a335cbe4765bc8ae80054391a80a5 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = 99b43a015d9a335cbe4765bc8ae80054391a80a5 && test "$(git rev-parse HEAD^{tree})" = 42ad69a45fc8fe87826667b28bb38d1b3a106253
WORKDIR /app
RUN /usr/local/cargo/bin/cargo build --tests
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
