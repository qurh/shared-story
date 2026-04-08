def test_search_story_first_with_fallback(client) -> None:
    response = client.get("/api/search?q=memory")
    assert response.status_code == 200
    body = response.json()
    assert "stories" in body["data"]
    assert "fallback" in body["data"]


def test_get_story_detail(client) -> None:
    response = client.get("/api/stories/story-1")
    assert response.status_code == 200
    assert response.json()["data"]["story"]["id"] == "story-1"


def test_subscribe_unsubscribe_story(client) -> None:
    subscribed = client.post("/api/stories/story-1/subscribe?user_id=u1")
    assert subscribed.status_code == 200
    assert subscribed.json()["data"]["subscribed"] is True

    unsubscribed = client.delete("/api/stories/story-1/subscribe?user_id=u1")
    assert unsubscribed.status_code == 200
    assert unsubscribed.json()["data"]["subscribed"] is False
