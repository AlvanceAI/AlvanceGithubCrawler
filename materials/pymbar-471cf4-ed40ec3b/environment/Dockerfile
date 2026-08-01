FROM docker.io/library/python:3.11
USER root
ENV HOME="/home/user"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python --version && /usr/local/bin/pip --version
RUN id -u user >/dev/null 2>&1 || useradd --create-home --shell /bin/bash user
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/choderalab/pymbar.git && git fetch --depth=1 origin ed40ec3bbef03bb08938ad1a74d459b0d1ab81f7 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = ed40ec3bbef03bb08938ad1a74d459b0d1ab81f7 && test "$(git rev-parse HEAD^{tree})" = da705aa87dd014f58741d74ceb08a19504cd1cb7
WORKDIR /app
RUN /usr/local/bin/pip install --no-cache-dir pytest
RUN /usr/local/bin/pip install --no-cache-dir -e .
RUN test -z "$(git status --porcelain)"
RUN chown -R user:user /app
USER root
WORKDIR /app
