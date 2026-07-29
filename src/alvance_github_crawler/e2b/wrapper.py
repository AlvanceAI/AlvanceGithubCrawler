from __future__ import annotations

import base64
import shlex
import time

import requests

from ..catalog.package_models import E2BWrapperReceipt, QualifiedRepository


class E2BHarborWrapperManager:
    """Prepare and validate Harbor-compatible aliases derived from repository templates."""

    def __init__(
        self,
        api_key: str,
        *,
        cpu_count: int = 2,
        memory_mb: int = 4_096,
    ) -> None:
        self.api_key = api_key
        self.cpu_count = cpu_count
        self.memory_mb = memory_mb

    def ensure(
        self,
        repository: QualifiedRepository,
        harbor_alias: str,
    ) -> E2BWrapperReceipt:
        try:
            from e2b import Template
        except ImportError as exc:
            raise RuntimeError("e2b SDK is required for Harbor packaging") from exc

        cache_hit = Template.alias_exists(harbor_alias, api_key=self.api_key)
        build_duration_s = 0.0
        if cache_hit:
            harbor_id = self.resolve_template_id(harbor_alias)
        else:
            builder = Template().from_template(repository.source_template_alias).set_workdir("/app")
            builder = add_runtime_wrappers(
                builder,
                repository.language,
                repository.runtime_env,
            )
            started = time.monotonic()
            info = Template.build(
                builder,
                name=harbor_alias,
                cpu_count=self.cpu_count,
                memory_mb=self.memory_mb,
                skip_cache=False,
                api_key=self.api_key,
            )
            build_duration_s = time.monotonic() - started
            harbor_id = info.template_id

        smoke = self.smoke(repository, harbor_alias)
        if not smoke["ok"]:
            raise RuntimeError(f"Harbor E2B wrapper smoke failed: {harbor_alias}")
        return E2BWrapperReceipt(
            source_template_id=self.resolve_template_id(repository.source_template_alias),
            harbor_template_id=harbor_id,
            harbor_template_alias=harbor_alias,
            cache_hit=cache_hit,
            build_duration_s=round(build_duration_s, 2),
            smoke=smoke,
        )

    def resolve_template_id(self, alias: str) -> str:
        response = requests.get(
            f"https://api.e2b.app/templates/aliases/{alias}",
            headers={"X-API-Key": self.api_key},
            timeout=30,
        )
        response.raise_for_status()
        return str(response.json()["templateID"])

    def smoke(
        self,
        repository: QualifiedRepository,
        harbor_alias: str,
    ) -> dict[str, object]:
        try:
            from e2b import Sandbox
        except ImportError as exc:
            raise RuntimeError("e2b SDK is required for Harbor packaging") from exc

        probe = runtime_probe(repository.language)
        command = (
            "cd /app && "
            f'test "$(git rev-parse HEAD)" = {shlex.quote(repository.base_commit)} '
            f"&& {probe}"
        )
        started = time.monotonic()
        with Sandbox.create(
            template=harbor_alias,
            allow_internet_access=False,
            timeout=120,
            api_key=self.api_key,
        ) as sandbox:
            result = sandbox.commands.run(
                command,
                user=repository.execution_user,
                timeout=60,
            )
        return {
            "ok": result.exit_code == 0,
            "user": repository.execution_user,
            "workdir": "/app",
            "base_commit": repository.base_commit,
            "runtime_probe": probe,
            "duration_s": round(time.monotonic() - started, 2),
            "sandbox_destroyed": True,
        }


def add_runtime_wrappers(
    builder: object,
    language: str,
    envs: dict[str, str],
) -> object:
    targets: dict[str, str] = {}
    if language == "go":
        targets = {
            "go": "/usr/local/go/bin/go",
            "gofmt": "/usr/local/go/bin/gofmt",
        }
    elif language == "rust":
        targets = {
            "cargo": "/usr/local/cargo/bin/cargo",
            "rustc": "/usr/local/cargo/bin/rustc",
            "rustup": "/usr/local/cargo/bin/rustup",
        }

    for name, target in targets.items():
        script = "#!/bin/sh\n" + "".join(
            f"export {key}={shlex.quote(value)}\n" for key, value in sorted(envs.items())
        )
        script += f'exec {target} "$@"\n'
        encoded = base64.b64encode(script.encode()).decode()
        builder = builder.run_cmd(
            f"printf %s {shlex.quote(encoded)} | base64 -d > /usr/local/bin/{name} "
            f"&& chmod 0755 /usr/local/bin/{name}",
            user="root",
        )
    return builder


def runtime_probe(language: str) -> str:
    if language == "go":
        return "go version"
    if language == "python":
        return "python --version"
    if language in {"typescript", "javascript"}:
        return "node --version"
    if language == "rust":
        return "cargo --version"
    raise ValueError(f"unsupported language: {language}")
