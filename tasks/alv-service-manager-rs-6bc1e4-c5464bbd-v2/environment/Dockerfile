FROM docker.io/library/rust:1.97.1
USER root
ENV CARGO_HOME="/usr/local/cargo"
ENV HOME="/root"
ENV PATH="/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV RUSTUP_HOME="/usr/local/rustup"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/cargo/bin/rustc --version && /usr/local/cargo/bin/cargo --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/chipsenkbeil/service-manager-rs.git && git fetch --depth=1 origin c5464bbd5d9f9b586d49581140ada7e3e9f01c61 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = c5464bbd5d9f9b586d49581140ada7e3e9f01c61 && test "$(git rev-parse HEAD^{tree})" = 9cb9fd17ff2c0677612ca216577cec5e9d305831
WORKDIR /app
RUN /usr/local/cargo/bin/cargo build --tests
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
