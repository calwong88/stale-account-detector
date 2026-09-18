from datetime import datetime, timedelta

from src.models import Account, UserType
from src.rules import rule_stale_signin

NOW = datetime(2026, 8, 31)


def test_stale_signin_flags_inactive_member():
    account = Account(
        upn="test@contoso.com",
        display_name="Test",
        enabled=True,
        user_type=UserType.MEMBER,
        created=datetime(2024, 1, 1),
        last_sign_in=datetime(2026, 1, 1),
        license_count=1,
        manager_upn="mgr@contoso.com",
    )
    finding = rule_stale_signin(account, NOW)
    assert finding is not None
    assert finding.rule_id == "IAM-001"


def test_stale_signin_does_not_flag_at_exactly_90_days():
    account = Account(
        upn="test_1@contoso.com",
        display_name="Test 1",
        enabled=True,
        user_type=UserType.MEMBER,
        created=datetime(2025, 1, 1),
        last_sign_in=NOW - timedelta(days=90),
        license_count=1,
        manager_upn="mgr_1@contoso.com",
    )
    finding = rule_stale_signin(account, NOW)
    assert finding is None