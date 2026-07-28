from sqlalchemy import text
from sqlalchemy.orm import Session


def get_threat_distribution(db: Session):
    result = db.execute(
        text("""
            SELECT
                severity,
                COUNT(*) AS total
            FROM alerts
            GROUP BY severity
            ORDER BY total DESC
        """)
    ).mappings().all()

    return result