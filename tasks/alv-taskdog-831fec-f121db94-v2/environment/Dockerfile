FROM docker.io/library/python:3.12
USER root
ENV HOME="/home/user"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python --version && /usr/local/bin/pip --version
RUN id -u user >/dev/null 2>&1 || useradd --create-home --shell /bin/bash user
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/Kohei-Wada/taskdog.git && git fetch --depth=1 origin f121db94017a100c0f792b3810e2591d49db9c39 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = f121db94017a100c0f792b3810e2591d49db9c39 && test "$(git rev-parse HEAD^{tree})" = 744749fc3eab68ca7ff5b78898c540e53a10fe36
WORKDIR /app
RUN /usr/local/bin/pip install --no-cache-dir pytest
RUN /usr/local/bin/pip install --no-cache-dir -e . -e packages/taskdog-client -e packages/taskdog-core -e packages/taskdog-mcp -e packages/taskdog-server -e packages/taskdog-ui
RUN /usr/local/bin/pip install --no-cache-dir -e '.[dev]'
RUN test -z "$(git status --porcelain)"
RUN chown -R user:user /app
USER root
WORKDIR /app
