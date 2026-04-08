from app.services.ranking_service import composite_score


def test_composite_score_penalizes_doubt() -> None:
    score_low_doubt = composite_score(
        subscribers=10,
        discussions=5,
        participants=4,
        views=100,
        doubt=0,
        age_hours=1,
    )
    score_high_doubt = composite_score(
        subscribers=10,
        discussions=5,
        participants=4,
        views=100,
        doubt=10,
        age_hours=1,
    )
    assert score_low_doubt > score_high_doubt
