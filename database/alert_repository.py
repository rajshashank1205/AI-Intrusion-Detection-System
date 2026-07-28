from datetime import datetime, timedelta

from database.connection import get_connection
from backend.websocket_events import broadcast_alert


# How long identical alerts should be suppressed
ALERT_COOLDOWN_SECONDS = 30


def save_alert(timestamp, source_ip, alert_type, severity, description):

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # ----------------------------------
        # Check for a recent duplicate alert
        # ----------------------------------

        cutoff_time = datetime.now() - timedelta(
            seconds=ALERT_COOLDOWN_SECONDS
        )

        duplicate_query = """
        SELECT id
        FROM alerts
        WHERE source_ip = %s
          AND alert_type = %s
          AND timestamp >= %s
        ORDER BY timestamp DESC
        LIMIT 1
        """

        cursor.execute(
            duplicate_query,
            (
                source_ip,
                alert_type,
                cutoff_time
            )
        )

        existing_alert = cursor.fetchone()

        # ----------------------------------
        # Duplicate found — don't save again
        # ----------------------------------

        if existing_alert:

            print(
                f"⏳ Duplicate alert suppressed: "
                f"{alert_type} from {source_ip}"
            )

            return False

        # ----------------------------------
        # Save new alert
        # ----------------------------------

        sql = """
        INSERT INTO alerts
        (
            timestamp,
            source_ip,
            alert_type,
            severity,
            description
        )
        VALUES (%s,%s,%s,%s,%s)
        """

        values = (
            timestamp,
            source_ip,
            alert_type,
            severity,
            description
        )

        cursor.execute(sql, values)

        conn.commit()

        print("🚨 Alert saved to MySQL.")
        print("🚨 Broadcasting alert to dashboard...")

        # Only genuinely new alerts reach the dashboard
        broadcast_alert({
            "timestamp": str(timestamp),
            "source_ip": source_ip,
            "alert_type": alert_type,
            "severity": severity,
            "description": description
        })

        return True

    except Exception as error:

        conn.rollback()

        print(
            f"❌ Failed to save alert: {error}"
        )

        return False

    finally:

        cursor.close()
        conn.close()