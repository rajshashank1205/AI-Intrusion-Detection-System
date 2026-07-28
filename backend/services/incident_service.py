from sqlalchemy import text
from sqlalchemy.orm import Session


def get_incidents(db: Session):

    # -----------------------------------
    # Create Missing Incident Records
    # -----------------------------------

    # Every unique source_ip + alert_type
    # combination becomes an incident.

    create_missing_incidents = text("""
        INSERT IGNORE INTO incidents (
            source_ip,
            attack_type,
            status
        )

        SELECT DISTINCT
            source_ip,
            alert_type,
            'OPEN'

        FROM alerts
    """)

    db.execute(
        create_missing_incidents
    )

    db.commit()


    # -----------------------------------
    # Get Incident Information
    # -----------------------------------

    query = text("""
        SELECT
            i.id,
            i.source_ip,
            i.attack_type,
            i.status,

            COUNT(a.source_ip)
                AS occurrence_count,

            MAX(a.timestamp)
                AS last_seen,

            CASE

                WHEN SUM(
                    CASE
                        WHEN a.severity = 'CRITICAL'
                        THEN 1
                        ELSE 0
                    END
                ) > 0
                THEN 'CRITICAL'


                WHEN SUM(
                    CASE
                        WHEN a.severity = 'HIGH'
                        THEN 1
                        ELSE 0
                    END
                ) > 0
                THEN 'HIGH'


                WHEN SUM(
                    CASE
                        WHEN a.severity = 'MEDIUM'
                        THEN 1
                        ELSE 0
                    END
                ) > 0
                THEN 'MEDIUM'


                ELSE 'LOW'

            END AS severity

        FROM incidents i

        LEFT JOIN alerts a

            ON
                i.source_ip = a.source_ip

            AND
                i.attack_type = a.alert_type


        GROUP BY

            i.id,
            i.source_ip,
            i.attack_type,
            i.status


        ORDER BY

            last_seen DESC


        LIMIT 100
    """)


    results = (
        db.execute(
            query
        )
        .mappings()
        .all()
    )


    incidents = []


    for incident in results:

        incidents.append({

            "id":
                incident["id"],

            "source_ip":
                incident["source_ip"],

            "attack_type":
                incident["attack_type"],

            "severity":
                incident["severity"],

            "occurrence_count":
                incident["occurrence_count"],

            "last_seen":
                incident["last_seen"],

            "status":
                incident["status"]

        })


    return incidents


# -----------------------------------
# Update Incident Status
# -----------------------------------

def update_incident_status(
    db: Session,
    incident_id: int,
    status: str
):

    allowed_statuses = [
        "OPEN",
        "INVESTIGATING",
        "RESOLVED"
    ]


    if status not in allowed_statuses:

        return None


    query = text("""
        UPDATE incidents

        SET status = :status

        WHERE id = :incident_id
    """)


    result = db.execute(
        query,
        {
            "status":
                status,

            "incident_id":
                incident_id
        }
    )


    db.commit()


    # Incident does not exist

    if result.rowcount == 0:

        return None


    return {

        "id":
            incident_id,

        "status":
            status

    }