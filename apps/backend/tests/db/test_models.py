from app.db.models import SubmissionTask


def test_submission_task_defaults() -> None:
    task = SubmissionTask(task_id="t1", target_type="insight", owner_role_id="r1")
    assert task.revision_count == 0
    assert task.status == "pending_review"
