from sqlalchemy import text


def get_top_hosts(db):
    query = text("""
        SELECT
            source_ip,
            COUNT(*) AS total
        FROM alerts
        GROUP BY source_ip
        ORDER BY total DESC
        LIMIT 5
    """)

    result = db.execute(query)

    return [
        {
            "source_ip": row.source_ip,
            "total": row.total,
        }
        for row in result
    ]