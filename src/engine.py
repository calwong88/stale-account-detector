from datetime import datetime

from src.models import Account, Finding
from src.rules import (
    rule_disabled_with_license,
    rule_never_signed_in,
    rule_no_manager,
    rule_pending_guest_invite,
    rule_stale_guest,
    rule_stale_signin,
)

ALL_RULES = [
    rule_stale_signin,
    rule_never_signed_in,
    rule_disabled_with_license,
    rule_no_manager,
    rule_pending_guest_invite,
    rule_stale_guest
]

def run_all(accounts: list[Account], now: datetime) -> list[Finding]:
    findings = []
    for rule in ALL_RULES:
        for account in accounts:
            finding = rule(account, now)
            if finding is not None:
                findings.append(finding)
    return findings
