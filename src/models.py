from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class Severity(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class UserType(Enum):
    MEMBER = "Member"
    GUEST = "Guest"


@dataclass
class Account:
    upn: str
    display_name: str
    enabled: bool
    user_type: UserType
    created: datetime
    last_sign_in: datetime | None   # None means never signed in
    license_count: int
    manager_upn: str | None
    guest_invite_pending: bool = False

    def days_since_sign_in(self, now: datetime) -> int | None:
        if self.last_sign_in is None:
            return None
        return (now - self.last_sign_in).days

    def days_since_created(self, now: datetime) -> int:
        return (now - self.created).days


@dataclass
class Finding:
    upn: str
    rule_id: str
    severity: Severity
    detail: str