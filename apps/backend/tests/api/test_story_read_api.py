def test_search_story_first_with_fallback(client) -> None:
    response = client.get("/api/v1/search?q=memory")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "stories" in body["data"]
    assert "fallback" in body["data"]
    assert body["error"] is None


def test_get_story_detail(client) -> None:
    response = client.get("/api/v1/stories/story-1")
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["story"]["id"] == "story-1"
    assert "activity_preview" in body["data"]["story"]
    assert "insights" in body["data"]["story"]["activity_preview"]
    assert "discussions" in body["data"]["story"]["activity_preview"]
    assert body["error"] is None


def test_subscribe_unsubscribe_story(client) -> None:
    subscribed = client.post("/api/v1/stories/story-1/subscribe?user_id=u1")
    assert subscribed.status_code == 200
    assert subscribed.json()["success"] is True
    assert subscribed.json()["data"]["subscribed"] is True
    assert subscribed.json()["error"] is None

    unsubscribed = client.delete("/api/v1/stories/story-1/subscribe?user_id=u1")
    assert unsubscribed.status_code == 200
    assert unsubscribed.json()["success"] is True
    assert unsubscribed.json()["data"]["subscribed"] is False
    assert unsubscribed.json()["error"] is None


def test_story_not_found_uses_error_schema(client) -> None:
    response = client.get("/api/v1/stories/not-exists")
    assert response.status_code == 404
    body = response.json()
    assert body["success"] is False
    assert body["data"] is None
    assert body["error"]["code"] == "NOT_FOUND"
    assert body["error"]["message"] == "Story not found"
