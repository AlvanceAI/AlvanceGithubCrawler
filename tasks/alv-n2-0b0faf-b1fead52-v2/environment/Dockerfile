FROM docker.io/library/rust:1.81.0
USER root
ENV CARGO_HOME="/usr/local/cargo"
ENV HOME="/root"
ENV PATH="/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV RUSTUP_HOME="/usr/local/rustup"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/cargo/bin/rustc --version && /usr/local/cargo/bin/cargo --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/evmar/n2.git && git fetch --depth=1 origin b1fead52ccda0c497d816696f23f4099c3e8ec1f && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = b1fead52ccda0c497d816696f23f4099c3e8ec1f && test "$(git rev-parse HEAD^{tree})" = b899aa8a8e3ab9bd8ac5de8b5d9744bfef25845f
WORKDIR /app
RUN /usr/local/cargo/bin/cargo build --tests
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
