from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.services.live_metrics import live_metrics


def get_dashboard_data(db: Session):

    # Total detected threats
    total_alerts = db.execute(
        text("SELECT COUNT(*) FROM alerts")
    ).scalar() or 0

    # Unique suspicious hosts
    connected_hosts = db.execute(
        text("""
            SELECT COUNT(DISTINCT source_ip)
            FROM alerts
        """)
    ).scalar() or 0

    # Real live packet rate
    packets_per_second = live_metrics.get_packet_rate()

    # Real latest AI anomaly score
    ai_score = live_metrics.get_ai_score()

    # Latest alerts
    recent_alerts = db.execute(
        text("""
            SELECT
                id,
                timestamp,
                source_ip,
                alert_type,
                severity,
                description
            FROM alerts
            ORDER BY timestamp DESC
            LIMIT 5
        """)
    ).mappings().all()

    return {
        "active_threats": total_alerts,
        "packets_per_second": packets_per_second,
        "connected_hosts": connected_hosts,
        "ai_confidence": ai_score,
        "recent_alerts": recent_alerts,
    }