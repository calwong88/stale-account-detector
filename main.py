import argparse
from datetime import datetime

from src.engine import run_all
from src.loader import load_accounts
from src.report import print_summary, write_csv


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect stale, orphaned, and over-licensed accounts in a directory export.")
    parser.add_argument("--input", default="data/users_sample.csv")
    parser.add_argument("--output", default="findings.csv")
    parser.add_argument("--as-of", default=None)
    args = parser.parse_args()

    accounts = load_accounts(args.input)

    if args.as_of is None:
        now = datetime.now()
    else:
        now = datetime.strptime(args.as_of, "%Y-%m-%d")

    findings = run_all(accounts, now)
    write_csv(findings, args.output)
    print_summary(findings)


if __name__ == "__main__":
    main()