from dataclasses import dataclass, field


@dataclass(slots=True)
class ReviewResult:
    code: str
    reason_code: str | None = None
    reason_text: str | None = None
    fix_actions: list[str] = field(default_factory=list)

    @property
    def approved(self) -> bool:
        return self.code == "APPROVED"
