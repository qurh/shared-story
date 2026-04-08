def test_resubmit_requires_owner(client) -> None:
    create_resp = client.post(
        "/api/v1/agent/insights",
        json={
            "story_id": "",
            "role_id": "agent-owner",
            "title": "invalid title",
            "summary": "invalid summary",
            "content": "invalid content to trigger rejection and create task",
        },
    )
    assert create_resp.status_code == 422
    assert create_resp.json()["success"] is False
    task_id = create_resp.json()["data"]["task_id"]

    response = client.post(
        f"/api/v1/agent/submissions/{task_id}/resubmit",
        json={
            "role_id": "other-agent",
            "story_id": "story-1",
            "title": "revised title",
            "summary": "revised summary",
            "content": "this is long enough and context-related content for approval",
        },
    )
    assert response.status_code == 403
    body = response.json()
    assert body["success"] is False
    assert body["error"]["code"] == "FORBIDDEN"


def test_submit_insight_rejected_has_reason_code(client) -> None:
    resp = client.post(
        "/api/v1/agent/insights",
        json={
            "story_id": "",
            "role_id": "agent-x",
            "title": "invalid",
            "summary": "invalid",
            "content": "invalid content for REJECTED_CONTEXT",
        },
    )
    assert resp.status_code == 422
    assert resp.json()["success"] is False
    data = resp.json()["data"]
    assert data["reason_code"] == "REJECTED_CONTEXT"
    assert len(data["fix_actions"]) > 0


def test_submit_insight_approved_and_review_result(client) -> None:
    create_resp = client.post(
        "/api/v1/agent/insights",
        json={
            "story_id": "story-1",
            "role_id": "agent-ok",
            "title": "approved insight",
            "summary": "approved summary",
            "content": "this is sufficiently long content and references story context for approval",
        },
    )
    assert create_resp.status_code == 200
    assert create_resp.json()["success"] is True
    task_id = create_resp.json()["data"]["task_id"]

    review_resp = client.get(f"/api/v1/agent/submissions/{task_id}/review-result")
    assert review_resp.status_code == 200
    assert review_resp.json()["success"] is True
    assert review_resp.json()["data"]["status"] == "approved"
