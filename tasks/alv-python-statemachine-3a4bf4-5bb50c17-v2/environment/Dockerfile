FROM docker.io/library/python:3.11
USER root
ENV HOME="/home/user"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python --version && /usr/local/bin/pip --version
RUN id -u user >/dev/null 2>&1 || useradd --create-home --shell /bin/bash user
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/fgmacedo/python-statemachine.git && git fetch --depth=1 origin 5bb50c177f296d2dc45c60538929b51464aecdff && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/develop HEAD && test "$(git rev-parse HEAD)" = 5bb50c177f296d2dc45c60538929b51464aecdff && test "$(git rev-parse HEAD^{tree})" = af245536fcf0f569162f07c1e20087e3b0365617
WORKDIR /app
RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade 'pip>=25.1'
RUN /usr/local/bin/pip install --no-cache-dir pytest
RUN /usr/local/bin/pip install --no-cache-dir --group dev
RUN /usr/local/bin/pip install --no-cache-dir -e .
RUN test -z "$(git status --porcelain)"
RUN chown -R user:user /app
USER root
WORKDIR /app
