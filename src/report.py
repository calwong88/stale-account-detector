import csv
from collections import Counter
from dataclasses import asdict

from src.models import Finding, Severity


def write_csv(findings: list[Finding], path: str) -> None:
    """Write a CSV file with the findings."""
    sorted_findings = sorted(findings, key=lambda f: (-f.severity.value, f.upn))
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["upn", "rule_id", "severity", "detail"])
        writer.writeheader()
        for finding in sorted_findings:
            row = asdict(finding)
            row["severity"] = finding.severity.name
            writer.writerow(row)


def print_summary(findings: list[Finding]) -> None:
    """Print a summary of the findings."""
    counts = Counter(f.severity for f in findings)
    print("Summary of Findings:")
    print(f" Total findings: {len(findings)}")
    for severity in sorted(Severity, key=lambda s: -s.value):
        count = counts[severity]
        print(f"  {severity.name}: {count}")
