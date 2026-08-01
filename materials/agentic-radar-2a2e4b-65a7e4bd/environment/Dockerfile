FROM docker.io/library/python:3.11
USER root
ENV HOME="/home/user"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python --version && /usr/local/bin/pip --version
RUN id -u user >/dev/null 2>&1 || useradd --create-home --shell /bin/bash user
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/splx-ai/agentic-radar.git && git fetch --depth=1 origin 65a7e4bd01e2034c7cb52e9620eeed287688cc53 && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = 65a7e4bd01e2034c7cb52e9620eeed287688cc53 && test "$(git rev-parse HEAD^{tree})" = 9e7ef2e3ff3da6e8b84d0e0731e24b5e1745f4b8
WORKDIR /app
RUN /usr/local/bin/pip install --no-cache-dir pytest
RUN /usr/local/bin/pip install --no-cache-dir poetry
RUN POETRY_VIRTUALENVS_CREATE=false /usr/local/bin/poetry install --no-interaction --no-root --with dev --all-extras
RUN /usr/local/bin/pip install --no-cache-dir -e .
RUN test -z "$(git status --porcelain)"
RUN chown -R user:user /app
USER root
WORKDIR /app
