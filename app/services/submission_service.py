from app.core.runtime_config import load_runtime_config
from app.db.models import SubmissionTask


class SubmissionService:
    def __init__(self) -> None:
        self.runtime_config = load_runtime_config()
        self.tasks: dict[str, SubmissionTask] = {}

    def create_task(self, *, owner_role_id: str, target_type: str, target_id: str | None = None) -> SubmissionTask:
        task = SubmissionTask(
            target_type=target_type,
            target_id=target_id,
            owner_role_id=owner_role_id,
            max_revisions=self.runtime_config.REVIEW_MAX_REVISIONS_PER_TASK,
            status="pending_review",
        )
        self.tasks[task.task_id] = task
        return task

    def get_task(self, task_id: str) -> SubmissionTask | None:
        return self.tasks.get(task_id)

    def submit(self, task_id: str) -> SubmissionTask | None:
        task = self.get_task(task_id)
        if not task:
            return None
        task.status = "pending_review"
        return task

    def reject_and_request_revision(self, task_id: str) -> SubmissionTask | None:
        task = self.get_task(task_id)
        if not task:
            return None
        task.revision_count += 1
        task.status = "rejected"
        return task

    def resubmit(self, task_id: str, role_id: str) -> SubmissionTask | None:
        task = self.get_task(task_id)
        if not task:
            return None
        if task.owner_role_id != role_id:
            return None
        if task.revision_count >= task.max_revisions:
            task.status = "revision_exhausted"
            return task
        task.status = "pending_review"
        return task
