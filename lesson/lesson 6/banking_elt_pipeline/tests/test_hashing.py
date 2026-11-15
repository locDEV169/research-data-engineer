from datetime import date, datetime, timezone
from decimal import Decimal

from etl.hashing import json_value, stable_record_hash


def test_json_value_converts_non_json_native_types():
    assert json_value(date(2026, 1, 1)) == "2026-01-01"
    assert json_value(Decimal("10.50")) == "10.50"
    assert json_value(datetime(2026, 1, 1, tzinfo=timezone.utc)) == "2026-01-01T00:00:00+00:00"
    assert json_value("plain string") == "plain string"


def test_stable_record_hash_ignores_key_order_and_extra_columns():
    record_a = {"id": 1, "name": "A", "noise": "ignored"}
    record_b = {"name": "A", "id": 1, "noise": "different-but-ignored"}

    hash_a = stable_record_hash(record_a, columns=["id", "name"])
    hash_b = stable_record_hash(record_b, columns=["id", "name"])

    assert hash_a == hash_b


def test_stable_record_hash_changes_when_tracked_value_changes():
    base = stable_record_hash({"id": 1, "name": "A"}, columns=["id", "name"])
    changed = stable_record_hash({"id": 1, "name": "B"}, columns=["id", "name"])

    assert base != changed
