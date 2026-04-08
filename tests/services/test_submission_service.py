from app.services.submission_service import SubmissionService


def test_resubmit_stops_at_revision_limit() -> None:
    service = SubmissionService()
    task = service.create_task(owner_role_id="agent-a", target_type="insight")

    service.reject_and_request_revision(task.task_id)
    service.resubmit(task.task_id, "agent-a")

    service.reject_and_request_revision(task.task_id)
    service.resubmit(task.task_id, "agent-a")

    service.reject_and_request_revision(task.task_id)
    blocked = service.resubmit(task.task_id, "agent-a")

    assert blocked.status == "revision_exhausted"


def test_resubmit_requires_owner() -> None:
    service = SubmissionService()
    task = service.create_task(owner_role_id="agent-a", target_type="insight")
    result = service.resubmit(task.task_id, "agent-b")
    assert result is None
