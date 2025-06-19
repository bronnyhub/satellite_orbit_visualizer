# fetch_data.py
from db_config import get_connection

def get_ephemeris(satellite_name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT timestamp, x, y, z FROM ephemeris WHERE satellite_name=%s ORDER BY timestamp",
        (satellite_name,)
    )
    data = cursor.fetchall()
    conn.close()
    return data
