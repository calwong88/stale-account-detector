# Stale Account Detector

Identity directories accumulate accounts that outlive their purpose: people leave, guest invitations go unanswered, and licenses stay assigned to accounts nobody uses. Each one is standing access that nobody is monitoring, and in regulated environments they surface as findings in SOX and OSFI access reviews. This tool evaluates a directory export against six detection rules and produces a severity-ranked report of accounts that need attention, with enough detail on each finding for a reviewer to act on it.

## Sample output

```
$ python main.py --as-of 2026-08-31
Summary of Findings:
 Total findings: 7
  HIGH: 2
  MEDIUM: 2
  LOW: 3
```

| upn | rule_id | severity | detail |
|---|---|---|---|
| never.signed@contoso.com | IAM-002 | HIGH | Account has never signed in since creation 426 days ago. |
| pending.guest@partner.com | IAM-002 | HIGH | Account has never signed in since creation 122 days ago. |
| stale.guest@partner.com | IAM-006 | MEDIUM | Guest account has not signed in for 169 days. |

## Detection rules

| Rule | Detects | Threshold | Severity |
|---|---|---|---|
| IAM-001 | Enabled member with no recent sign-in | > 90 days | MEDIUM |
| IAM-002 | Enabled account never signed in since creation | > 30 days since creation | HIGH |
| IAM-003 | Disabled account still holding paid licenses | any license | LOW |
| IAM-004 | Enabled member with no manager assigned | — | LOW |
| IAM-005 | Guest invitation never redeemed | > 14 days | LOW |
| IAM-006 | Enabled guest with no recent sign-in | > 45 days | MEDIUM |

## Design decisions

**The loader is the only code that sees raw CSV.** Every CSV value arrives as a string, so the loader converts each field to its proper type before building an `Account` object — including a deliberate bool parser, since `bool("False")` is `True` in Python. Rules, the engine, and the report only ever work with typed `Account` objects. That boundary means a Microsoft Graph loader could replace the CSV loader without changing any other module.

**Rules receive the evaluation date instead of checking today's date.** Every rule takes `now` as a parameter rather than calling `datetime.now()` internally. This makes reports reproducible — `--as-of` regenerates a past report exactly, and the sample output above matches for anyone who runs the same command — and it keeps tests stable, since they pin a fixed date and never drift.

**Guests and members are evaluated by separate staleness rules.** Applying IAM-001 to every account meant a stale guest was flagged twice, by IAM-001 and the guest-specific IAM-006. IAM-001 is now scoped to members and IAM-006 owns guests, so each problem produces exactly one finding. Guests get a shorter threshold (45 days versus 90) because external identities have no HR offboarding process to catch their departure. Tests enforce the split in both directions.

**Never-used accounts are rated HIGH.** An account that was created and never signed into is an enabled credential with no owner watching it. These accounts often still hold their initial password and have never registered MFA, which makes them attractive targets — and because there is no normal activity to compare against, misuse would be hard to spot.

**The sample data includes deliberate near-misses.** `new.hire@contoso.com` has never signed in, just like `never.signed@contoso.com`, but was created five days ago — within the 30-day grace period. It exists to prove the tool doesn't flag new employees before their start date. Every rule has a matching negative test for the same reason: a detection tool that fires on everything gets ignored.

## Usage

Requires Python 3.10+. No runtime dependencies beyond the standard library.

```
git clone https://github.com/calwong88/stale-account-detector.git
cd stale-account-detector
python main.py
```

| Flag | Default | Purpose |
|---|---|---|
| `--input` | `data/users_sample.csv` | Directory export to evaluate |
| `--output` | `findings.csv` | Where to write the findings report |
| `--as-of` | today | Evaluation date (`YYYY-MM-DD`), for reproducible reports |

### Running tests

```
pip install -r requirements-dev.txt
pytest
```

## Limitations and next steps

- CSV input only. A Microsoft Graph loader using `signInActivity` would let this run against a live tenant. The loader boundary means no other module changes.
- Thresholds are module constants. Moving them to a config file would let each organization tune them to its own policy.
- Early `--as-of` dates aren't validated. A date earlier than the data produces negative day counts, which happen to fail every threshold check rather than being rejected with a clear error.
- Non-interactive sign-ins aren't considered. Service and token-based activity can keep an account legitimately in use without an interactive sign-in, which a Graph-based loader would need to account for.