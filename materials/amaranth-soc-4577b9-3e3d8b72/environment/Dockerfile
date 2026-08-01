FROM docker.io/library/python:3.11
USER root
ENV HOME="/home/user"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python --version && /usr/local/bin/pip --version
RUN id -u user >/dev/null 2>&1 || useradd --create-home --shell /bin/bash user
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/amaranth-lang/amaranth-soc.git && git fetch --depth=1 origin 3e3d8b7241c1c7e80e0cd12937d288d0ad4a6cba && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = 3e3d8b7241c1c7e80e0cd12937d288d0ad4a6cba && test "$(git rev-parse HEAD^{tree})" = 505f27aeb436f8d1b0a2f9bc5c30fe73d20a5848
WORKDIR /app
RUN /usr/local/bin/pip install --no-cache-dir pytest
RUN /usr/local/bin/pip install --no-cache-dir -e .
RUN test -z "$(git status --porcelain)"
RUN chown -R user:user /app
USER root
WORKDIR /app
