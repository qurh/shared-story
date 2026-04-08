from typer.testing import CliRunner

from agent_cli.main import app


def test_submit_insight_command() -> None:
    runner = CliRunner()
    result = runner.invoke(
        app,
        [
            "submit-insight",
            "--story-id",
            "s1",
            "--role-id",
            "r1",
            "--title",
            "t",
            "--summary",
            "s",
            "--content",
            "c",
        ],
    )
    assert result.exit_code == 0
