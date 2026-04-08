from app.review.engine import review_submission


def test_review_rejects_missing_story_context() -> None:
    result = review_submission(story_id="", title="标题", summary="摘要", content="内容内容内容内容内容内容")
    assert result.code == "REJECTED_CONTEXT"
    assert len(result.fix_actions) > 0


def test_review_rejects_missing_structure() -> None:
    result = review_submission(story_id="story-1", title="", summary="", content="")
    assert result.code == "REJECTED_STRUCTURE"


def test_review_approves_valid_submission() -> None:
    result = review_submission(
        story_id="story-1",
        title="我的解读",
        summary="这是摘要",
        content="这是一个长度足够并且围绕故事上下文展开的有效内容，用于通过审核。",
    )
    assert result.code == "APPROVED"
