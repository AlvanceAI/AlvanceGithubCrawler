# Harbor rebuildable envelope v2
# Dockerfile recipe v3
# E2B aliases are optional caches; this file is the durable build source.
FROM docker.io/library/rust:1.85
USER root
ENV CARGO_HOME="/usr/local/cargo"
ENV HOME="/root"
ENV PATH="/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV RUSTUP_HOME="/usr/local/rustup"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/cargo/bin/rustc --version && /usr/local/cargo/bin/cargo --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/assert-rs/assert_fs.git && git fetch --depth=1 origin e2bce9fcc4268a92f30fed0218e8695865dafa15 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = e2bce9fcc4268a92f30fed0218e8695865dafa15 && test "$(git rev-parse HEAD^{tree})" = eea1fcd2ae26407882fd67fbc90c5f8cd049dafc
WORKDIR /app
RUN /usr/local/cargo/bin/cargo build --tests
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
