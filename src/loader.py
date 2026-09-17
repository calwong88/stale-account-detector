import csv
from datetime import datetime

from src.models import Account, UserType


def _parse_date(value: str) -> datetime:
    """CSV dates are date-only, so parse them as naive datetimes."""
    return datetime.strptime(value.strip(), "%Y-%m-%d")

def _to_bool(value: str) -> bool:
    """Convert a CSV string like 'True'/'false' into a real bool."""
    return value.strip().lower() == "true"


def _to_optional_str(value: str) -> str | None:
    """Blank cells become None, so Optional[str] means what it says."""
    return value.strip() if value.strip() else None


def _to_optional_date(value: str) -> datetime | None:
    """Blank cells become None; otherwise parse YYYY-MM-DD."""
    return _parse_date(value) if value.strip() else None


def load_accounts(path: str) -> list[Account]:
    accounts = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            account = Account(
                upn=row["upn"].strip(),
                display_name=row["display_name"].strip(),
                enabled=_to_bool(row["enabled"]),
                user_type=UserType(row["user_type"].strip()),
                created=_parse_date(row["created"]),
                last_sign_in=_to_optional_date(row["last_sign_in"]),
                license_count=int(row["license_count"]),
                manager_upn=_to_optional_str(row["manager_upn"]),
                guest_invite_pending=_to_bool(row["guest_invite_pending"]),
            )
            accounts.append(account)
    return accounts

