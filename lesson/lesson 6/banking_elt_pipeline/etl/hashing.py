import hashlib
import json
from datetime import UTC, date, datetime
from decimal import Decimal


def json_value(value):
    if isinstance(value, datetime):
        return value.astimezone(UTC).isoformat() if value.tzinfo else value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    return value


def json_rows(rows):
    return [{key: json_value(value) for key, value in row.items()} for row in rows]


def stable_record_hash(record, columns):
    data = {column: record.get(column) for column in columns}
    text = json.dumps(data, sort_keys=True, default=str, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()
