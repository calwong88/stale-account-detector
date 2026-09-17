from datetime import datetime

from src.models import Account, Finding, Severity, UserType

STALE_SIGNIN_DAYS = 90
NEVER_SIGNIN_GRACE_DAYS = 30
PENDING_INVITE_DAYS = 14
STALE_GUEST_DAYS = 45


def rule_stale_signin(account: Account, now: datetime) -> Finding | None:
    """
    IAM-001: Enabled member-only account with no sign-in activity in more than 90 days.
    Severity: MEDIUM.
    Returns a Finding, or None if the account is clean under this rule.
    """
    if not account.enabled:
        return None
    if account.user_type != UserType.MEMBER:
        return None
    days_since_sign_in = account.days_since_sign_in(now)
    if days_since_sign_in is None or days_since_sign_in <= STALE_SIGNIN_DAYS:
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
    if account.last_sign_in is not None:
        return None
    days_since_creation = account.days_since_created(now)
    if days_since_creation <= NEVER_SIGNIN_GRACE_DAYS:
        return None
    detail = f"Account has never signed in since creation {days_since_creation} days ago."
    return Finding(
        upn=account.upn,
        rule_id="IAM-002",
        severity=Severity.HIGH,
        detail=detail,
    )


def rule_disabled_with_license(account: Account, now: datetime) -> Finding | None:
    """
    IAM-003: Disabled account still consuming a paid license.
    """
    if account.enabled:
        return None
    if account.license_count <= 0:
        return None
    detail = f"Disabled account is still consuming {account.license_count} paid licenses."
    return Finding(
        upn=account.upn,
        rule_id="IAM-003",
        severity=Severity.LOW,
        detail=detail,
    )


def rule_no_manager(account: Account, now: datetime) -> Finding | None:
    """
    IAM-004: Enabled member account with no manager assigned.
    """
    if not account.enabled:
        return None
    if account.user_type != UserType.MEMBER:
        return None
    if account.manager_upn is not None:
        return None
    detail = "Enabled member account has no manager assigned."
    return Finding(
        upn=account.upn,
        rule_id="IAM-004",
        severity=Severity.LOW,
        detail=detail,
    )


def rule_pending_guest_invite(account: Account, now: datetime) -> Finding | None:
    """
    IAM-005: Guest invitation issued but never accepted.
    """
    if not account.enabled:
        return None
    if account.user_type != UserType.GUEST:
        return None
    if not account.guest_invite_pending:
        return None
    days_pending = account.days_since_created(now)
    if days_pending <= PENDING_INVITE_DAYS:
        return None
    detail = f"Guest invitation is pending and has not been accepted for {days_pending} days."
    return Finding(
        upn=account.upn,
        rule_id="IAM-005",
        severity=Severity.LOW,
        detail=detail,
    )


def rule_stale_guest(account: Account, now: datetime) -> Finding | None:
    """
    IAM-006: Guest account with no recent sign-in activity.
    """
    if not account.enabled:
        return None
    if account.user_type != UserType.GUEST:
        return None
    days_since_sign_in = account.days_since_sign_in(now)
    if days_since_sign_in is None or days_since_sign_in <= STALE_GUEST_DAYS:
        return None
    detail = f"Guest account has not signed in for {days_since_sign_in} days."
    return Finding(
        upn=account.upn,
        rule_id="IAM-006",
        severity=Severity.MEDIUM,
        detail=detail,
    )

