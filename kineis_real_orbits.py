from sgp4.api import Satrec, jday
from datetime import datetime, timedelta

satellites = {
    "KINEIS-4A": (
        "1 63303U 25056D   25162.43713416  .00001388  00000+0  22719-3 0  9991",
        "2 63303  97.9819 288.3012 0003546  62.3034 297.8533 14.72338745 12576"
    ),
    # Add other TLEs here...
}

with open("kineis_real_orbits.sql", "w") as f:
    f.write("CREATE DATABASE IF NOT EXISTS satellite_data;\nUSE satellite_data;\n")
    f.write("""
CREATE TABLE IF NOT EXISTS ephemeris (
    id INT AUTO_INCREMENT PRIMARY KEY,
    satellite_name VARCHAR(100),
    timestamp DATETIME,
    x DOUBLE,
    y DOUBLE,
    z DOUBLE
);\n""")

    for name, (l1, l2) in satellites.items():
        sat = Satrec.twoline2rv(l1, l2)
        for mins in range(0, 91, 10):
            dt = datetime(2025, 6, 11, 0, 0) + timedelta(minutes=mins)
            jd, fr = jday(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
            e, r, _ = sat.sgp4(jd, fr)
            if e == 0:
                f.write(f"INSERT INTO ephemeris (satellite_name, timestamp, x, y, z) VALUES "
                        f"('{name}', '{dt.strftime('%Y-%m-%d %H:%M:%S')}', {r[0]}, {r[1]}, {r[2]});\n")
