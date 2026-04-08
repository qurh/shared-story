def test_resubmit_requires_owner(client) -> None:
    create_resp = client.post(
        "/api/agent/insights",
        json={
            "story_id": "",
            "role_id": "agent-owner",
            "title": "标题",
            "summary": "摘要",
            "content": "这是用于触发驳回并创建任务的文本内容。",
        },
    )
    assert create_resp.status_code == 422
    task_id = create_resp.json()["data"]["task_id"]

    response = client.post(
        f"/api/agent/submissions/{task_id}/resubmit",
        json={
            "role_id": "other-agent",
            "story_id": "story-1",
            "title": "修订标题",
            "summary": "修订摘要",
            "content": "这是修订后的合规长文本内容，用于通过审核。",
        },
    )
    assert response.status_code == 403


def test_submit_insight_rejected_has_reason_code(client) -> None:
    resp = client.post(
        "/api/agent/insights",
        json={
            "story_id": "",
            "role_id": "agent-x",
            "title": "标题",
            "summary": "摘要",
            "content": "这是一段用于触发 REJECTED_CONTEXT 的文本内容。",
        },
    )
    assert resp.status_code == 422
    data = resp.json()["data"]
    assert data["reason_code"] == "REJECTED_CONTEXT"
    assert len(data["fix_actions"]) > 0


def test_submit_insight_approved_and_review_result(client) -> None:
    create_resp = client.post(
        "/api/agent/insights",
        json={
            "story_id": "story-1",
            "role_id": "agent-ok",
            "title": "通过审核的解读",
            "summary": "这是摘要",
            "content": "这是一个长度足够并且围绕故事上下文展开的有效内容，用于通过审核。",
        },
    )
    assert create_resp.status_code == 200
    task_id = create_resp.json()["data"]["task_id"]

    review_resp = client.get(f"/api/agent/submissions/{task_id}/review-result")
    assert review_resp.status_code == 200
    assert review_resp.json()["data"]["status"] == "approved"
