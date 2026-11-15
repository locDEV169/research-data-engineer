"""Buoc data quality check: duplicate, null key, reconciliation raw vs clean."""

from .clients import connect_bigquery, run_sql_file
from .settings import PROJECT_ROOT, load_config

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


def run():
    config = load_config()
    client = connect_bigquery(config)

    print("Running data quality checks...")
    rows = run_sql_file(client, config, PROJECT_ROOT / "sql" / "04_checks.sql")
    failures = []

    for row in rows:
        check_name = row["check_name"]
        issue_count = int(row["issue_count"])
        if issue_count == 0:
            print(f"  {GREEN}PASS{RESET}: {check_name}")
        else:
            print(f"  {RED}FAIL{RESET}: {check_name} issue_count={issue_count}")
            failures.append(f"{check_name}={issue_count}")

    if failures:
        print(f"{RED}Checks FAILED: {', '.join(failures)}{RESET}")
        print(f"{RED}Watermark da duoc ghi o buoc 02 va KHONG duoc rollback.{RESET}")
        raise SystemExit(1)

    print(f"{GREEN}All checks PASS.{RESET}")


if __name__ == "__main__":
    run()
