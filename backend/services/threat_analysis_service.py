from sqlalchemy import text
from sqlalchemy.orm import Session


def get_threat_analysis(db: Session):

    # Latest detected threats
    threats = db.execute(
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
            LIMIT 100
        """)
    ).mappings().all()

    # Severity counts
    severity_counts = {
        "CRITICAL": 0,
        "HIGH": 0,
        "MEDIUM": 0,
        "LOW": 0,
    }

    for threat in threats:

        severity = threat["severity"]

        if severity in severity_counts:
            severity_counts[severity] += 1

    # Calculate overall threat score
    severity_weights = {
        "CRITICAL": 100,
        "HIGH": 75,
        "MEDIUM": 50,
        "LOW": 25,
    }

    if threats:

        total_score = sum(
            severity_weights.get(
                threat["severity"],
                0
            )
            for threat in threats
        )

        threat_score = round(
            total_score / len(threats)
        )

    else:
        threat_score = 0

    return {
        "threat_score": threat_score,
        "total_threats": len(threats),
        "severity_counts": severity_counts,
        "latest_threats": [
            dict(threat)
            for threat in threats
        ],
    }