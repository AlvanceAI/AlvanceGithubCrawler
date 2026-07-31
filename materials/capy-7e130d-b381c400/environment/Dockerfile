FROM docker.io/library/rust:1.88
USER root
ENV CARGO_HOME="/usr/local/cargo"
ENV HOME="/root"
ENV PATH="/usr/local/cargo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
ENV RUSTUP_HOME="/usr/local/rustup"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/cargo/bin/rustc --version && /usr/local/cargo/bin/cargo --version
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/capy-language/capy.git && git fetch --depth=1 origin b381c400d4db4d6058d7579addf04a0b9825e941 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = b381c400d4db4d6058d7579addf04a0b9825e941 && test "$(git rev-parse HEAD^{tree})" = 494ca6f0d81c615fcea4561180717ebbebd193b1
WORKDIR /app
RUN /usr/local/cargo/bin/cargo build --tests
RUN test -z "$(git status --porcelain)"
USER root
WORKDIR /app
