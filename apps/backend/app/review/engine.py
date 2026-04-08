from app.review.types import ReviewResult


COMPLIANCE_TERMS = ("非法", "违法", "illegal", "terrorism")


def _rejected(code: str, reason_text: str, fix_actions: list[str]) -> ReviewResult:
    return ReviewResult(
        code=code,
        reason_code=code,
        reason_text=reason_text,
        fix_actions=fix_actions[:3],
    )


def review_submission(
    *,
    story_id: str,
    title: str,
    summary: str,
    content: str,
) -> ReviewResult:
    if not story_id.strip():
        return _rejected(
            "REJECTED_CONTEXT",
            "缺少 Story 上下文，无法确认内容锚点。",
            [
                "补充有效的 story_id。",
                "确保内容围绕具体 Story 叙述。",
            ],
        )

    if not title.strip() or not summary.strip() or not content.strip():
        return _rejected(
            "REJECTED_STRUCTURE",
            "缺少最小结构字段（标题/摘要/正文）。",
            [
                "补全标题、摘要和正文字段。",
                "摘要建议概括核心观点。",
            ],
        )

    lowered = content.lower()
    if any(term in lowered for term in COMPLIANCE_TERMS):
        return _rejected(
            "REJECTED_COMPLIANCE",
            "内容存在疑似合规风险词汇。",
            [
                "删除或替换高风险描述。",
                "改为中性、可核验表达。",
            ],
        )

    if len(content.strip()) < 30:
        return _rejected(
            "REJECTED_QUALITY",
            "正文过短，信息量不足。",
            [
                "补充关键论据或上下文引用。",
                "明确你的判断依据。",
            ],
        )

    return ReviewResult(code="APPROVED")
