from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class Story(Base):
    __tablename__ = "stories"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(32), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, onupdate=now_utc)


class Insight(Base):
    __tablename__ = "insights"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    story_id: Mapped[str] = mapped_column(String(64), ForeignKey("stories.id"))
    role_id: Mapped[str] = mapped_column(String(64))
    title: Mapped[str] = mapped_column(String(255))
    summary: Mapped[str] = mapped_column(Text, default="")
    content: Mapped[str] = mapped_column(Text)
    version: Mapped[int] = mapped_column(Integer, default=1)
    status: Mapped[str] = mapped_column(String(32), default="pending_review")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class Discussion(Base):
    __tablename__ = "discussions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    story_id: Mapped[str] = mapped_column(String(64), ForeignKey("stories.id"))
    insight_id: Mapped[str | None] = mapped_column(String(64), ForeignKey("insights.id"), nullable=True)
    role_id: Mapped[str] = mapped_column(String(64))
    content: Mapped[str] = mapped_column(Text)
    reply_to_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="pending_review")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class ReviewRecord(Base):
    __tablename__ = "review_records"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    target_type: Mapped[str] = mapped_column(String(32))
    target_id: Mapped[str] = mapped_column(String(64))
    result: Mapped[str] = mapped_column(String(32))
    reason_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reason_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    fix_actions: Mapped[str | None] = mapped_column(Text, nullable=True)
    revision_count: Mapped[int] = mapped_column(Integer, default=0)
    reviewer_type: Mapped[str] = mapped_column(String(32), default="system")
    reviewed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class SubmissionTask(Base):
    __tablename__ = "submission_tasks"

    task_id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    target_type: Mapped[str] = mapped_column(String(32))
    target_id: Mapped[str | None] = mapped_column(String(64), nullable=True)
    owner_role_id: Mapped[str] = mapped_column(String(64))
    revision_count: Mapped[int] = mapped_column(Integer, default=0)
    max_revisions: Mapped[int] = mapped_column(Integer, default=3)
    status: Mapped[str] = mapped_column(String(32), default="pending_review")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, onupdate=now_utc)

    def __init__(
        self,
        task_id: str | None = None,
        target_type: str = "",
        target_id: str | None = None,
        owner_role_id: str = "",
        revision_count: int = 0,
        max_revisions: int = 3,
        status: str = "pending_review",
    ) -> None:
        self.task_id = task_id or str(uuid4())
        self.target_type = target_type
        self.target_id = target_id
        self.owner_role_id = owner_role_id
        self.revision_count = revision_count
        self.max_revisions = max_revisions
        self.status = status


class Subscription(Base):
    __tablename__ = "subscriptions"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    story_id: Mapped[str] = mapped_column(String(64), ForeignKey("stories.id"))
    user_id: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc)


class ContentMetrics(Base):
    __tablename__ = "content_metrics"

    id: Mapped[str] = mapped_column(String(64), primary_key=True, default=lambda: str(uuid4()))
    story_id: Mapped[str] = mapped_column(String(64), ForeignKey("stories.id"))
    view_count: Mapped[int] = mapped_column(Integer, default=0)
    discussion_count: Mapped[int] = mapped_column(Integer, default=0)
    participant_role_count: Mapped[int] = mapped_column(Integer, default=0)
    subscriber_count: Mapped[int] = mapped_column(Integer, default=0)
    doubt_count: Mapped[int] = mapped_column(Integer, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now_utc, onupdate=now_utc)
