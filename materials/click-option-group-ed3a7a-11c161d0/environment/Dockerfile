FROM docker.io/library/python:3.11
USER root
ENV HOME="/home/user"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python --version && /usr/local/bin/pip --version
RUN id -u user >/dev/null 2>&1 || useradd --create-home --shell /bin/bash user
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/click-contrib/click-option-group.git && git fetch --depth=1 origin 11c161d0f66768510f45459a38e673a00b1918d8 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/master HEAD && test "$(git rev-parse HEAD)" = 11c161d0f66768510f45459a38e673a00b1918d8 && test "$(git rev-parse HEAD^{tree})" = 2a1638472c6050a4fda4db86304f85ac3bac07bd
WORKDIR /app
RUN /usr/local/bin/pip install --no-cache-dir pytest
RUN /usr/local/bin/pip install --no-cache-dir -e '.[test,dev,test-cov]'
RUN test -z "$(git status --porcelain)"
RUN chown -R user:user /app
USER root
WORKDIR /app
