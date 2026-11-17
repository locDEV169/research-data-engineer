-- Câu 8 (optional): Tỷ lệ giao dịch thất bại (%) theo từng kênh.
-- Kênh đáng lo nhất = tỷ lệ fail cao nhất (ORDER BY DESC).

SELECT
    ch.channel_name,
    COUNT(*) AS tong_gd,
    COUNT(*) FILTER (WHERE t.status = 'FAILED') AS so_fail,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE t.status = 'FAILED') / NULLIF(COUNT(*), 0),
        2
    ) AS ty_le_fail_pct
FROM transactions AS t
INNER JOIN channels AS ch
    ON ch.channel_id = t.channel_id
GROUP BY ch.channel_name
ORDER BY ty_le_fail_pct DESC NULLS LAST;
