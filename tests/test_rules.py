from datetime import datetime, timedelta

from src.models import Account, UserType
from src.rules import (
    rule_stale_signin,
    rule_never_signed_in,
    rule_disabled_with_license
)


NOW = datetime(2026, 8, 31)

def make_account(**overrides) -> Account:
    defaults = {
        "upn": "test@contoso.com",
        "display_name": "Test",
        "enabled": True,
        "user_type": UserType.MEMBER,
        "created": NOW - timedelta(days=365),
        "last_sign_in": NOW - timedelta(days=1),
        "license_count": 1,
        "manager_upn": "mgr@contoso.com",
        "guest_invite_pending": False,
    }
    return Account(**{**defaults, **overrides})


def test_stale_signin_flags_inactive_member():
    account = make_account(last_sign_in=datetime(2026, 1, 1))
    finding = rule_stale_signin(account, NOW)
    assert finding is not None
    assert finding.rule_id == "IAM-001"


def test_stale_signin_does_not_flag_at_exactly_90_days():
    account = make_account(last_sign_in=NOW - timedelta(days=90))
    finding = rule_stale_signin(account, NOW)
    assert finding is None


def test_never_signed_in_flags_past_grace_period():
    account = make_account(
            created=NOW - timedelta(days=31),
            last_sign_in=None,
        )
    finding = rule_never_signed_in(account, NOW)
    assert finding is not None
    assert finding.rule_id == "IAM-002"


def test_never_signed_in_does_not_flag_within_grace_period():
    account = make_account(
            created=NOW - timedelta(days=20),
            last_sign_in=None,
        )
    finding = rule_never_signed_in(account, NOW)
    assert finding is None


def test_disabled_with_license_flags_disabled_account_with_licenses():
    account = make_account(
            enabled=False,
            license_count=5
        )
    finding = rule_disabled_with_license(account, NOW)
    assert finding is not None
    assert finding.rule_id == "IAM-003"


def test_disabled_with_license_does_not_flag_when_no_licenses():
    account = make_account(
            enabled=False,
            license_count=0
        )
    finding = rule_disabled_with_license(account, NOW)
    assert finding is None


def test_disabled_with_license_does_not_flag_enabled_account():
    account = make_account(
            enabled=True,
            license_count=0
        )
    finding = rule_disabled_with_license(account, NOW)
    assert finding is None

