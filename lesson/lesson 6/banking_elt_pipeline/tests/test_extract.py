from etl.extract import build_extract_query, to_dataframe

SAMPLE_TABLE = {
    "name": "branches",
    "watermark": "updated_at",
    "columns": {"branch_id": "INT64", "branch_name": "STRING", "updated_at": "TIMESTAMP"},
}


def test_build_extract_query_without_watermark_selects_everything():
    sql = build_extract_query(SAMPLE_TABLE, last_watermark=None)

    assert "WHERE" not in sql
    assert sql.startswith("SELECT branch_id, branch_name, updated_at FROM branches")
    assert sql.endswith("ORDER BY updated_at")


def test_build_extract_query_with_watermark_filters_newer_rows():
    sql = build_extract_query(SAMPLE_TABLE, last_watermark="2026-01-01 00:00:00")

    assert "WHERE updated_at > '2026-01-01 00:00:00'" in sql


def test_to_dataframe_keeps_declared_column_order():
    rows = [{"updated_at": "t1", "branch_id": 1, "branch_name": "HN"}]

    df = to_dataframe(SAMPLE_TABLE, rows)

    assert list(df.columns) == ["branch_id", "branch_name", "updated_at"]
    assert df.iloc[0]["branch_id"] == 1
