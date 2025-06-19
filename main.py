
import mysql.connector
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# --- Connect to MySQL with known password ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bronny"
)
cursor = db.cursor()

# --- Create and select database ---
cursor.execute("CREATE DATABASE IF NOT EXISTS satellite_data")
cursor.execute("USE satellite_data")

# --- Create ephemeris table if not exists ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS ephemeris (
    id INT AUTO_INCREMENT PRIMARY KEY,
    satellite_name VARCHAR(100),
    timestamp DATETIME,
    x DOUBLE,
    y DOUBLE,
    z DOUBLE
)
""")
db.commit()

# --- Fetch data from ephemeris ---
def get_ephemeris(sat_name):
    cursor.execute(
        "SELECT timestamp, x, y, z FROM ephemeris WHERE satellite_name=%s ORDER BY timestamp",
        (sat_name,)
    )
    return cursor.fetchall()

# --- Plot satellite orbit ---
def plot_orbit(data, sat_name):
    if not data:
        print(f"No data for satellite '{sat_name}'")
        return

    x = [row[1] for row in data]
    y = [row[2] for row in data]
    z = [row[3] for row in data]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(x, y, z, label=sat_name)
    ax.scatter([0], [0], [0], color='blue', label='Earth')
    ax.set_xlabel('X (km)')
    ax.set_ylabel('Y (km)')
    ax.set_zlabel('Z (km)')
    ax.set_title(f'Orbit of {sat_name}')
    ax.legend()
    plt.show()

# --- Main program loop ---
if __name__ == "__main__":
    print("📡 Satellite Orbit Visualizer")
    name = input("Enter satellite name (e.g., KINEIS-2A): ").strip().upper()
    data = get_ephemeris(name)
    plot_orbit(data, name)
