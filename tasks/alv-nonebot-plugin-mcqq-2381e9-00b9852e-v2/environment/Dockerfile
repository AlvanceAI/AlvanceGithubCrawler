FROM docker.io/library/python:3.11
USER root
ENV HOME="/home/user"
ENV PATH="/usr/local/bin:/usr/local/sbin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN apt-get update && apt-get install -y --no-install-recommends time git ca-certificates build-essential && rm -rf /var/lib/apt/lists/*
RUN /usr/local/bin/python --version && /usr/local/bin/pip --version
RUN id -u user >/dev/null 2>&1 || useradd --create-home --shell /bin/bash user
WORKDIR /
RUN rm -rf /app && mkdir -p /app && git init /app && cd /app && git remote add origin https://github.com/17TheWord/nonebot-plugin-mcqq.git && git fetch --depth=1 origin 00b9852e32387ad742e68984410f2dda308c866c && git checkout --detach FETCH_HEAD && git submodule update --init --recursive && git update-ref refs/remotes/origin/main HEAD && test "$(git rev-parse HEAD)" = 00b9852e32387ad742e68984410f2dda308c866c && test "$(git rev-parse HEAD^{tree})" = d361aaff66158da328640a1fcea27022b3709e0e
WORKDIR /app
RUN /usr/local/bin/python -m pip install --no-cache-dir --upgrade 'pip>=25.1'
RUN /usr/local/bin/pip install --no-cache-dir pytest
RUN /usr/local/bin/pip install --no-cache-dir --group test
RUN /usr/local/bin/pip install --no-cache-dir --group dev
RUN /usr/local/bin/pip install --no-cache-dir -e .
RUN test -z "$(git status --porcelain)"
RUN chown -R user:user /app
USER root
WORKDIR /app
