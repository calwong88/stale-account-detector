from datetime import datetime

from src.models import Account, Finding, Severity

STALE_SIGNIN_DAYS = 90
NEVER_SIGNIN_GRACE_DAYS = 30

def rule_stale_signin(account: Account, now: datetime) -> Finding | None:
    """
    IAM-001: Enabled account with no sign-in activity in more than 90 days.
    Severity: MEDIUM.
    Returns a Finding, or None if the account is clean under this rule.
    """
    if not account.enabled:
        return None
    days_since_sign_in = account.days_since_sign_in(now)
    if days_since_sign_in is None or days_since_sign_in <= 90:
        return None
    detail = f"Account has not signed in for {days_since_sign_in} days."
    return Finding(
        upn=account.upn,
        rule_id="IAM-001",
        severity=Severity.MEDIUM,
        detail=detail,

    )

def rule_never_signed_in(account: Account, now: datetime) -> Finding | None:
    """
    IAM-002: Enabled account that has never been used since creation.
    """
    if not account.enabled:
        return None
    days_since_creation = account.days_since_created(now)
    if days_since_creation is None or days_since_creation <= NEVER_SIGNIN_GRACE_DAYS:
        return None
    if account.last_sign_in is not None:
        return None
    detail = f"Account has never signed in since creation {days_since_creation} days ago."
    return Finding(
        upn=account.upn,
        rule_id="IAM-002",
        severity=Severity.MEDIUM,
        detail=detail,
    )

def rule_disabled_with_license(account: Account, now: datetime) -> Finding | None:
    """
    IAM-003: Disabled account still consuming a paid license.
    """
    if account.enabled:
        return None
    if account.enabled is not None and account.license_count > 0:
        detail = f"Disabled account is still consuming {account.license_count} paid licenses."
        return Finding(
            upn=account.upn,
            rule_id="IAM-003",
            severity=Severity.LOW,
            detail=detail,
        ) 