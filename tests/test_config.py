from __future__ import annotations

from alvance_github_crawler.config import PipelineConfig, normalize_openai_base_url


def test_normalize_openai_base_url() -> None:
    assert normalize_openai_base_url("http://model.example:3003") == (
        "http://model.example:3003/v1"
    )
    assert normalize_openai_base_url("https://model.example/openai/v1/") == (
        "https://model.example/openai/v1"
    )


def test_external_env_aliases(tmp_path, monkeypatch) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "MODEL_API_KEY=model-key\n"
        "MODEL_BASE_URL=http://model.example/v1\n"
        "MODEL_NAME=custom-model\n"
        "E2B_KEY=e2b-key\n",
        encoding="utf-8",
    )
    for key in (
        "OPENAI_API_KEY",
        "OPENAI_BASE_URL",
        "OPENAI_MODEL",
        "E2B_API_KEY",
        "E2B_API_KEY1",
        "E2B_API_KEY2",
        "E2B_API_KEY3",
        "MODEL_API_KEY",
        "MODEL_BASE_URL",
        "MODEL_NAME",
        "E2B_KEY",
        "PIPELINE_ENV_FILE",
    ):
        monkeypatch.delenv(key, raising=False)
    monkeypatch.setenv("PIPELINE_ENV_FILE", str(env_file))
    # Prevent auto-loading the project's .env file during tests
    monkeypatch.chdir(tmp_path)

    config = PipelineConfig.from_env()
    assert config.openai_api_key == "model-key"
    assert config.openai_base_url == "http://model.example/v1"
    assert config.openai_model == "custom-model"
    assert config.e2b_api_key == "e2b-key"
    assert config.e2b_api_keys == ("e2b-key",)


def test_e2b_resource_and_concurrency_config(monkeypatch) -> None:
    monkeypatch.setenv("PIPELINE_E2B_CPU_COUNT", "1")
    monkeypatch.setenv("PIPELINE_E2B_MEMORY_MB", "1024")
    monkeypatch.setenv("PIPELINE_E2B_CONCURRENCY", "20")
    monkeypatch.setenv("PIPELINE_PRESCREEN_CONCURRENCY", "8")
    monkeypatch.setenv("PIPELINE_LANGUAGE_QUOTA_ENABLED", "false")

    config = PipelineConfig.from_env()

    assert config.e2b_cpu_count == 1
    assert config.e2b_memory_mb == 1024
    assert config.e2b_concurrency == 20
    assert config.prescreen_concurrency == 8
    assert config.language_quota_enabled is False
    config.validate(require_e2b=False)


def test_numbered_e2b_keys_create_independent_concurrency_pools(monkeypatch) -> None:
    monkeypatch.delenv("E2B_API_KEY", raising=False)
    monkeypatch.delenv("E2B_KEY", raising=False)
    monkeypatch.setenv("E2B_API_KEY1", "first-key")
    monkeypatch.setenv("E2B_API_KEY2", "second-key")
    monkeypatch.setenv("E2B_API_KEY3", "third-key")
    monkeypatch.setenv("PIPELINE_E2B_CONCURRENCY", "20")

    config = PipelineConfig.from_env()

    assert config.e2b_api_keys == ("first-key", "second-key", "third-key")
    assert config.e2b_api_key == "first-key"
    assert config.e2b_total_concurrency == 60
    config.validate(require_e2b=True)
