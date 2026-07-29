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
