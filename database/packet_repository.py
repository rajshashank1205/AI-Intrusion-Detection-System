from database.connection import get_connection


def save_packet(packet_data):

    conn = get_connection()
    cursor = conn.cursor()

    sql = """
    INSERT INTO packets
    (
        timestamp,
        source_ip,
        destination_ip,
        source_port,
        destination_port,
        protocol,
        packet_size,
        ttl,
        tcp_flags
    )

    VALUES
    (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    values = (
        packet_data["timestamp"],
        packet_data["src_ip"],
        packet_data["dst_ip"],
        packet_data["src_port"],
        packet_data["dst_port"],
        packet_data["protocol"],
        packet_data["packet_size"],
        packet_data["ttl"],
        packet_data["flags"]
    )

    cursor.execute(sql, values)

    conn.commit()

    cursor.close()
    conn.close()