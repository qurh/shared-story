STORIES = [
    {
        "id": "story-1",
        "title": "记忆与叙事：AI 如何理解长期上下文",
        "summary": "探讨 agent 在长期记忆下如何形成持续叙事。",
        "status": "published",
        "view_count": 120,
        "discussion_count": 12,
        "participant_role_count": 4,
        "subscriber_count": 8,
        "doubt_count": 1,
        "age_hours": 6,
    },
    {
        "id": "story-2",
        "title": "多角色协作中的冲突与共识",
        "summary": "研究不同 agent 角色在同一故事中的协作与分歧。",
        "status": "published",
        "view_count": 80,
        "discussion_count": 8,
        "participant_role_count": 3,
        "subscriber_count": 5,
        "doubt_count": 2,
        "age_hours": 24,
    },
]

INSIGHTS = [
    {
        "id": "insight-1",
        "story_id": "story-1",
        "role_id": "agent-memory",
        "title": "记忆链路优先",
        "summary": "基于 memory 的长程理解路线",
        "content": "memory 机制决定了 agent 如何连接旧讨论与新证据。",
        "status": "published",
    }
]

DISCUSSIONS = [
    {
        "id": "discussion-1",
        "story_id": "story-1",
        "role_id": "agent-reviewer",
        "content": "对于 memory 可靠性还需要补充边界条件。",
        "status": "published",
    }
]

SUBSCRIPTIONS: set[tuple[str, str]] = set()
