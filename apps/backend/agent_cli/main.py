import json

import typer

from agent_cli.client import SharedStoryClient

app = typer.Typer(help="shared-story OpenClaw Agent CLI")


@app.command("submit-insight")
def submit_insight(
    story_id: str = typer.Option(..., "--story-id"),
    role_id: str = typer.Option(..., "--role-id"),
    title: str = typer.Option(..., "--title"),
    summary: str = typer.Option(..., "--summary"),
    content: str = typer.Option(..., "--content"),
) -> None:
    payload = {
        "story_id": story_id,
        "role_id": role_id,
        "title": title,
        "summary": summary,
        "content": content,
    }
    result = SharedStoryClient().submit_insight(payload)
    typer.echo(json.dumps(result, ensure_ascii=False))


@app.command("submit-discussion")
def submit_discussion(
    story_id: str = typer.Option(..., "--story-id"),
    role_id: str = typer.Option(..., "--role-id"),
    content: str = typer.Option(..., "--content"),
) -> None:
    payload = {
        "story_id": story_id,
        "role_id": role_id,
        "content": content,
    }
    result = SharedStoryClient().submit_discussion(payload)
    typer.echo(json.dumps(result, ensure_ascii=False))


@app.command("resubmit")
def resubmit(
    task_id: str = typer.Option(..., "--task-id"),
    story_id: str = typer.Option(..., "--story-id"),
    role_id: str = typer.Option(..., "--role-id"),
    title: str = typer.Option(..., "--title"),
    summary: str = typer.Option(..., "--summary"),
    content: str = typer.Option(..., "--content"),
) -> None:
    payload = {
        "story_id": story_id,
        "role_id": role_id,
        "title": title,
        "summary": summary,
        "content": content,
    }
    result = SharedStoryClient().resubmit(task_id, payload)
    typer.echo(json.dumps(result, ensure_ascii=False))


@app.command("review-result")
def review_result(task_id: str = typer.Option(..., "--task-id")) -> None:
    result = SharedStoryClient().review_result(task_id)
    typer.echo(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    app()
