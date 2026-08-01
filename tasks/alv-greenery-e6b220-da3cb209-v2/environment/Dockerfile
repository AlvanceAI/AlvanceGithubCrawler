FROM docker.io/library/python:3.11
USER root
ENV HOME="/home/user"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python --version && /usr/local/bin/pip --version
RUN id -u user >/dev/null 2>&1 || useradd --create-home --shell /bin/bash user
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/qntm/greenery.git && git fetch --depth=1 origin da3cb2092178357bb089de842a20ec2a8053b889 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = da3cb2092178357bb089de842a20ec2a8053b889 && test "$(git rev-parse HEAD^{tree})" = 7b4e1be0fc1a374e42b44f7a0026af8d2f73d2a4
WORKDIR /app
RUN /usr/local/bin/pip install --no-cache-dir pytest
RUN /usr/local/bin/pip install --no-cache-dir -e .
RUN test -z "$(git status --porcelain)"
RUN chown -R user:user /app
USER root
WORKDIR /app
