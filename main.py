### I resign from doing the SQL part, because of the problems with recalculating data. 
### With SQL in use, the orbits would shown weirdly (they would not appear as a oval)

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sgp4.api import Satrec, jday
from datetime import datetime, timedelta, timezone
import numpy as np
from matplotlib.colors import LightSource

tle_data = {
    "KINEIS-2A": (
        "1 62932U 25028E   25070.18603320  .00002712  00000+0  39695-3 0  9992",
        "2 62932  97.9520 125.5704 0002314 177.9065 182.2155 14.76452397  4461"
    ),
    "KINEIS-2B": (
        "1 62934U 25028G   25070.18370421  .00003040  00000+0  44270-3 0  9997",
        "2 62934  97.9518 125.5732 0002807 160.1255 200.0064 14.76586491  4464"
    ),
    "KINEIS-2C": (
        "1 62929U 25028B   25070.19584427  .00002953  00000+0  43614-3 0  9998",
        "2 62929  97.9519 125.5574 0000226 139.0080 221.1147 14.76001819  4469"
    ),
    "KINEIS-2D": (
        "1 62930U 25028C   25070.19403799  .00000140  00000+0  27638-4 0  9997",
        "2 62930  97.9518 125.5594 0000542 185.2961 174.8243 14.76069104  4477"
    ),
    "KINEIS-2E": (
        "1 62931U 25028D   25070.19223928  .00002871  00000+0  42266-3 0  9998",
        "2 62931  97.9516 125.5619 0001390 125.6487 234.4852 14.76155257  4471"
    ),
    "KINEIS-4A": (
        "1 63303U 25056D   25162.43713416  .00001388  00000+0  22719-3 0  9991",
        "2 63303  97.9819 288.3012 0003546  62.3034 297.8533 14.72338745 12576"
    ),
     "KINEIS-4B": (
        "1 63304U 25056E   25162.55378811  .00001297  00000+0  21234-3 0  9991",
        "2 63304  97.9820 288.4602 0003193  42.2075 317.9378 14.72437290 12582"
    ),
    "KINEIS-4C": (
        "1 63301U 25056B   25162.46997488  .00001346  00000+0  22064-3 0  9992",
        "2 63301  97.9818 288.4135 0002817  95.5013 264.6515 14.72329417 12584"
    ),
    "KINEIS-4D": (
        "1 63302U 25056C   25162.46586770  .00001345  00000+0  22065-3 0  9991",
        "2 63302  97.9818 288.4185 0003060  88.2349 271.9209 14.72299173 12588"
    ),
    "KINEIS-4E": (
        "1 63300U 25056A   25162.45321942  .00001320  00000+0  21630-3 0  9996",
        "2 63300  97.9819 288.2800 0001978  76.7214 283.4214 14.72377699 12571"
    )
}

def compute_orbit(name, minutes=90):
    line1, line2 = tle_data[name]
    sat = Satrec.twoline2rv(line1, line2)
    positions = []

    start_time = datetime.now(timezone.utc)  
    for i in range(minutes):
        t = start_time + timedelta(minutes=i)
        jd, fr = jday(t.year, t.month, t.day, t.hour, t.minute, t.second)
        e, r, _ = sat.sgp4(jd, fr)
        if e == 0:
            positions.append(r)  # x, y, z in km
    return positions

def create_sphere(radius, resolution=20):
    """Create sphere with texture coordinates"""
    phi = np.linspace(0, np.pi, resolution)
    theta = np.linspace(0, 2*np.pi, resolution)
    phi, theta = np.meshgrid(phi, theta)

    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)
    
    return x, y, z

def plot_earth(ax, radius=6371):
    x, y, z = create_sphere(radius, 50)
    
    ls = LightSource(azdeg=135, altdeg=45)
    rgb = np.ones((x.shape[0], x.shape[1], 3))
    rgb[:,:,:] = np.array([0.1, 0.3, 0.8])
    
    shade = ls.shade_normals(np.dstack((x, y, z)), fraction=0.8)
    shade = shade[..., np.newaxis] 
    earth = ax.plot_surface(x, y, z, facecolors=rgb*shade, 
                       rstride=1, cstride=1, alpha=0.7, 
                       linewidth=0, antialiased=True,
                       zorder=0)
    
    theta = np.linspace(0, 2*np.pi, 100)
    for lat in np.linspace(-np.pi/2, np.pi/2, 7):
        x_c = radius * np.cos(lat) * np.cos(theta)
        y_c = radius * np.cos(lat) * np.sin(theta)
        z_c = radius * np.sin(lat) * np.ones_like(theta)
        ax.plot(x_c, y_c, z_c, color='0.2', alpha=0.1, linewidth=0.5)
    
    for lon in np.linspace(0, 2*np.pi, 12):
        x_c = radius * np.cos(theta) * np.cos(lon)
        y_c = radius * np.cos(theta) * np.sin(lon)
        z_c = radius * np.sin(theta)
        ax.plot(x_c, y_c, z_c, color='0.2', alpha=0.1, linewidth=0.5)
    
    return earth

def animate_orbit(positions, name):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_title(f"Animated Orbit: {name}", fontsize=14, pad=20)
    
    max_range = 8000
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)
    
    ax.set_xlabel("X (km)", fontsize=10, labelpad=10)
    ax.set_ylabel("Y (km)", fontsize=10, labelpad=10)
    ax.set_zlabel("Z (km)", fontsize=10, labelpad=10)
    
    ax.grid(True, alpha=0.3)
    
    earth = plot_earth(ax)
    earth.set_alpha(0.4)
    
    xs, ys, zs = [], [], []
    line, = ax.plot([], [], [], color='red', linewidth=1.5, label=f'{name} Orbit', zorder=10)
    point, = ax.plot([], [], [], 'o', color='yellow', markersize=6, label=f'{name} Position', zorder=10)
    
    ax.legend(loc='upper right', fontsize=9)
    ax.view_init(elev=25, azim=45)
    
    info_text = ax.text2D(0.02, 0.95, "", transform=ax.transAxes, fontsize=9)
    
    def update(i):
        if i < len(positions):
            x, y, z = positions[i]
            xs.append(x)
            ys.append(y)
            zs.append(z)
            
            line.set_data(xs, ys)
            line.set_3d_properties(zs)
            
            point.set_data([x], [y])
            point.set_3d_properties([z])
            
            info_text.set_text(f"Position: {i+1}/{len(positions)}\nX: {x:.1f} km\nY: {y:.1f} km\nZ: {z:.1f} km")
            
        return line, point, info_text
    
    ani = FuncAnimation(fig, update, frames=len(positions), interval=100, blit=False)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    print("📡 Kinéis Orbit Visualizer")
    sat_choice = input("Choose satellite (2A-E or 4A-E): ").strip().upper()
    name = f"KINEIS-{sat_choice}"

    if name in tle_data:
        positions = compute_orbit(name)
        animate_orbit(positions, name)
    else:
        print("Satellite not found.")