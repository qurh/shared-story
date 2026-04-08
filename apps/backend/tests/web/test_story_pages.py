def test_story_feed_page_renders(client) -> None:
    response = client.get("/stories")
    assert response.status_code == 404


def test_story_detail_page_renders(client) -> None:
    response = client.get("/stories/story-1")
    assert response.status_code == 404
