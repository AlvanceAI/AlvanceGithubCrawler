FROM docker.io/library/rust:1.97.1
USER root
ENV CARGO_HOME="/usr/local/cargo"
ENV HOME="/root"
ENV PATH="/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV RUSTUP_HOME="/usr/local/rustup"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/cargo/bin/rustc --version && /usr/local/cargo/bin/cargo --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/metaplex-foundation/sugar.git && git fetch --depth=1 origin f63f54a73591f7a7befc1a72fc30e9b8070154ed && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = f63f54a73591f7a7befc1a72fc30e9b8070154ed && test "$(git rev-parse HEAD^{tree})" = 04fc3c01675917023a366b7915617184f1132f8d
WORKDIR /app
RUN /usr/local/cargo/bin/cargo build --tests
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
