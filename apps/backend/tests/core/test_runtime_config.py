from app.core.runtime_config import load_runtime_config


def test_load_runtime_config() -> None:
    cfg = load_runtime_config("config.phase1_runtime")
    assert cfg.REVIEW_MAX_REVISIONS_PER_TASK == 3
    assert cfg.DEFAULT_SORT == "composite"
