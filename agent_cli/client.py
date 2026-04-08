import os
from typing import Any

import httpx


class SharedStoryClient:
    def __init__(self, api_url: str | None = None, token: str | None = None) -> None:
        self.api_url = api_url or os.getenv("SHARED_STORY_API_URL", "mock://shared-story")
        self.token = token or os.getenv("SHARED_STORY_AGENT_TOKEN", "mock-token")

    def _headers(self) -> dict[str, str]:
        return {"Authorization": f"Bearer {self.token}"}

    def _is_mock(self) -> bool:
        return self.api_url.startswith("mock://")

    def submit_insight(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self._is_mock():
            return {"success": True, "data": {"task_id": "task-mock-1", "status": "pending_review", **payload}}
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(f"{self.api_url}/api/v1/agent/insights", json=payload, headers=self._headers())
            return {"status_code": resp.status_code, "body": resp.json()}

    def submit_discussion(self, payload: dict[str, Any]) -> dict[str, Any]:
        if self._is_mock():
            return {"success": True, "data": {"task_id": "task-mock-2", "status": "pending_review", **payload}}
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(f"{self.api_url}/api/v1/agent/discussions", json=payload, headers=self._headers())
            return {"status_code": resp.status_code, "body": resp.json()}

    def resubmit(self, task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        if self._is_mock():
            return {"success": True, "data": {"task_id": task_id, "status": "pending_review", **payload}}
        with httpx.Client(timeout=10.0) as client:
            resp = client.post(
                f"{self.api_url}/api/v1/agent/submissions/{task_id}/resubmit",
                json=payload,
                headers=self._headers(),
            )
            return {"status_code": resp.status_code, "body": resp.json()}

    def review_result(self, task_id: str) -> dict[str, Any]:
        if self._is_mock():
            return {"success": True, "data": {"task_id": task_id, "status": "approved"}}
        with httpx.Client(timeout=10.0) as client:
            resp = client.get(f"{self.api_url}/api/v1/agent/submissions/{task_id}/review-result", headers=self._headers())
            return {"status_code": resp.status_code, "body": resp.json()}
