"""Chạy lần lượt các file SQL trong part1_sql/ trên Postgres source.

Cách dùng (từ folder BTVN_6):
    cp ../Lesson_6_Lab_production/.env .env   # hoặc tự điền
    source .venv/bin/activate
    pip install 'psycopg[binary]' python-dotenv
    python run_part1.py
    python run_part1.py q01_customers_hanoi.sql
"""

import sys
from pathlib import Path

import psycopg  # pyright: ignore[reportMissingImports]
from dotenv import dotenv_values  # pyright: ignore[reportMissingImports]
from psycopg.rows import dict_row  # pyright: ignore[reportMissingImports]

ROOT = Path(__file__).resolve().parent
SQL_DIR = ROOT / "part1_sql"
LAB_ENV = ROOT.parent / "Lesson_6_Lab_production" / ".env"


def load_env():
    for path in (ROOT / ".env", LAB_ENV):
        if path.exists():
            return dotenv_values(path), path
    raise FileNotFoundError(
        "Không tìm thấy .env (BTVN_6/.env hoặc Lesson_6_Lab_production/.env)"
    )


def connect():
    env, path = load_env()
    print(f"Using env: {path}")
    dsn = (
        f"host={env['SOURCE_DB_HOST']} port={env['SOURCE_DB_PORT']} "
        f"dbname={env['SOURCE_DB_NAME']} user={env['SOURCE_DB_USER']} "
        f"password={env['SOURCE_DB_PASSWORD']} connect_timeout=15"
    )
    return psycopg.connect(dsn, row_factory=dict_row)


def sql_files(only_name=None):
    if only_name:
        path = SQL_DIR / only_name
        if not path.exists():
            raise FileNotFoundError(path)
        return [path]
    return sorted(SQL_DIR.glob("q*.sql"))


def run_file(conn, path: Path, preview=5):
    sql = path.read_text(encoding="utf-8")
    print(f"\n=== {path.name} ===")
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
        print(f"rows={len(rows)}")
        for row in rows[:preview]:
            print(dict(row))
        if len(rows) > preview:
            print(f"... ({len(rows) - preview} more)")
    return len(rows)


def main():
    only = sys.argv[1] if len(sys.argv) > 1 else None
    with connect() as conn:
        for path in sql_files(only):
            run_file(conn, path)
    print("\nDone.")


if __name__ == "__main__":
    main()
