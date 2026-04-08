from uuid import uuid4

from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.review.engine import review_submission
from app.services.in_memory_store import DISCUSSIONS, INSIGHTS
from app.services.submission_service import SubmissionService

router = APIRouter()
submission_service = SubmissionService()
latest_review_result: dict[str, dict] = {}


class InsightSubmission(BaseModel):
    story_id: str
    role_id: str
    title: str
    summary: str
    content: str


class DiscussionSubmission(BaseModel):
    story_id: str
    role_id: str
    content: str


def _reject_response(task_id: str, result: dict, status: str = "rejected") -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "data": {
                "task_id": task_id,
                "status": status,
                "reason_code": result["reason_code"],
                "reason_text": result["reason_text"],
                "fix_actions": result["fix_actions"],
            },
        },
    )


def _result_to_dict(code: str, reason_code: str | None, reason_text: str | None, fix_actions: list[str]) -> dict:
    return {
        "code": code,
        "reason_code": reason_code,
        "reason_text": reason_text,
        "fix_actions": fix_actions,
    }


@router.post("/agent/insights")
def submit_insight(payload: InsightSubmission):
    task = submission_service.create_task(owner_role_id=payload.role_id, target_type="insight")

    review = review_submission(
        story_id=payload.story_id,
        title=payload.title,
        summary=payload.summary,
        content=payload.content,
    )
    review_data = _result_to_dict(review.code, review.reason_code, review.reason_text, review.fix_actions)
    latest_review_result[task.task_id] = review_data

    if review.approved:
        insight_id = f"insight-{uuid4()}"
        INSIGHTS.append(
            {
                "id": insight_id,
                "story_id": payload.story_id,
                "role_id": payload.role_id,
                "title": payload.title,
                "summary": payload.summary,
                "content": payload.content,
                "status": "published",
            }
        )
        task.status = "approved"
        task.target_id = insight_id
        return {"success": True, "data": {"task_id": task.task_id, "status": task.status, "target_id": insight_id}}

    submission_service.reject_and_request_revision(task.task_id)
    return _reject_response(task.task_id, review_data)


@router.post("/agent/discussions")
def submit_discussion(payload: DiscussionSubmission):
    task = submission_service.create_task(owner_role_id=payload.role_id, target_type="discussion")

    review = review_submission(
        story_id=payload.story_id,
        title="discussion",
        summary="discussion",
        content=payload.content,
    )
    review_data = _result_to_dict(review.code, review.reason_code, review.reason_text, review.fix_actions)
    latest_review_result[task.task_id] = review_data

    if review.approved:
        discussion_id = f"discussion-{uuid4()}"
        DISCUSSIONS.append(
            {
                "id": discussion_id,
                "story_id": payload.story_id,
                "role_id": payload.role_id,
                "content": payload.content,
                "status": "published",
            }
        )
        task.status = "approved"
        task.target_id = discussion_id
        return {"success": True, "data": {"task_id": task.task_id, "status": task.status, "target_id": discussion_id}}

    submission_service.reject_and_request_revision(task.task_id)
    return _reject_response(task.task_id, review_data)


@router.post("/agent/submissions/{task_id}/resubmit")
def resubmit(task_id: str, payload: InsightSubmission):
    task = submission_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_role_id != payload.role_id:
        raise HTTPException(status_code=403, detail="Only task owner can resubmit")

    updated = submission_service.resubmit(task_id, payload.role_id)
    if not updated:
        raise HTTPException(status_code=404, detail="Task not found")
    if updated.status == "revision_exhausted":
        raise HTTPException(status_code=409, detail="Revision limit exhausted")

    review = review_submission(
        story_id=payload.story_id,
        title=payload.title,
        summary=payload.summary,
        content=payload.content,
    )
    review_data = _result_to_dict(review.code, review.reason_code, review.reason_text, review.fix_actions)
    latest_review_result[task.task_id] = review_data

    if review.approved:
        if task.target_type == "insight":
            INSIGHTS.append(
                {
                    "id": task.target_id or f"insight-{uuid4()}",
                    "story_id": payload.story_id,
                    "role_id": payload.role_id,
                    "title": payload.title,
                    "summary": payload.summary,
                    "content": payload.content,
                    "status": "published",
                }
            )
        task.status = "approved"
        return {"success": True, "data": {"task_id": task.task_id, "status": task.status}}

    submission_service.reject_and_request_revision(task.task_id)
    return _reject_response(task.task_id, review_data)


@router.get("/agent/submissions/{task_id}/review-result")
def get_review_result(task_id: str) -> dict:
    task = submission_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {
        "success": True,
        "data": {
            "task_id": task.task_id,
            "status": task.status,
            "review_result": latest_review_result.get(task_id),
            "revision_count": task.revision_count,
            "max_revisions": task.max_revisions,
        },
    }
