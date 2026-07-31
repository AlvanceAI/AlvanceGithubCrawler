FROM docker.io/library/rust:1.97.1
USER root
ENV CARGO_HOME="/usr/local/cargo"
ENV HOME="/root"
ENV PATH="/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV RUSTUP_HOME="/usr/local/rustup"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/cargo/bin/rustc --version && /usr/local/cargo/bin/cargo --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/rcoh/angle-grinder.git && git fetch --depth=1 origin 9c2fc8846d7e950160579ef0b2d7ca56a76688e9 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = 9c2fc8846d7e950160579ef0b2d7ca56a76688e9 && test "$(git rev-parse HEAD^{tree})" = 90baef5aeea107f2f7b9198e90dd919af2a8fd3f
WORKDIR /app
RUN /usr/local/cargo/bin/cargo build --tests
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
