# Harbor rebuildable envelope v2
# Dockerfile recipe v3
# E2B aliases are optional caches; this file is the durable build source.
FROM docker.io/library/rust:1.97.1
USER root
ENV CARGO_HOME="/usr/local/cargo"
ENV HOME="/root"
ENV PATH="/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV RUSTUP_HOME="/usr/local/rustup"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/cargo/bin/rustc --version && /usr/local/cargo/bin/cargo --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/printfn/fend.git && git fetch --depth=1 origin f2d7ff49feeaaddcdbdbad147e8b152aefcb9e5e && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = f2d7ff49feeaaddcdbdbad147e8b152aefcb9e5e && test "$(git rev-parse HEAD^{tree})" = 629ddeb559593de3139cafef1c7d8bed2c1d7eb6
WORKDIR /app
RUN /usr/local/cargo/bin/cargo build --tests
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
