from datetime import datetime
from typing import Optional
from src.models import Account, Finding, Severity

STALE_SIGNIN_DAYS = 90

def rule_stale_signin(account: Account, now: datetime) -> Optional[Finding]:
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