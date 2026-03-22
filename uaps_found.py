import math
import webbrowser
import os

def haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371.0
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)
    
    a = math.sin(dphi/2.0)**2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda/2.0)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def evaluate_kinematic_track(track_coords, lat_axis, lon_axis, t_axis, v_min=2.0, a_min=50.0):
    if len(track_coords) < 3:
        return False
        
    t_vals = [t_axis[t_idx] for t_idx, _, _ in track_coords]
    lats = [lat_axis[lat_idx] for _, lat_idx, _ in track_coords]
    lons = [lon_axis[lon_idx] for _, _, lon_idx in track_coords]
    
    velocities = []
    vector_vx = []
    vector_vy = []
    
    for i in range(len(t_vals)-1):
        dt = t_vals[i+1] - t_vals[i]
        if dt == 0: dt = 1e-9
        
        dy = (lats[i+1] - lats[i]) * 111.32
        dx = (lons[i+1] - lons[i]) * 111.32 * math.cos(math.radians(lats[i]))
        
        vx = dx / dt
        vy = dy / dt
        speed = math.sqrt(vx**2 + vy**2)
        
        vector_vx.append(vx)
        vector_vy.append(vy)
        velocities.append(speed)
        
    accel_g_vals = []
    for i in range(len(velocities)-1):
        dt_mid = ((t_vals[i+2] - t_vals[i+1]) + (t_vals[i+1] - t_vals[i])) / 2.0
        dvx = vector_vx[i+1] - vector_vx[i]
        dvy = vector_vy[i+1] - vector_vy[i]
        
        accel_mag = math.sqrt(dvx**2 + dvy**2) / dt_mid
        accel_g = accel_mag / 0.00980665
        accel_g_vals.append(accel_g)
        
    is_hypersonic = max(velocities) >= v_min if velocities else False
    is_high_g = max(accel_g_vals) >= a_min if accel_g_vals else False
    
    return bool(is_hypersonic and is_high_g)

def evaluate_multimodal_signature(track_coords, optical_tensor, IR_tensor, radar_tensor, velocity_array):
    # Pure python replacement for tensor arrays
    t_idx = [t for t, _, _ in track_coords]
    y_idx = [y for _, y, _ in track_coords]
    x_idx = [x for _, _, x in track_coords]
    
    opt_sig = [optical_tensor[t][y][x] for t, y, x in zip(t_idx, y_idx, x_idx)]
    ir_sig = [IR_tensor[t][y][x] for t, y, x in zip(t_idx, y_idx, x_idx)]
    rad_sig = [radar_tensor[t][y][x] for t, y, x in zip(t_idx, y_idx, x_idx)]
    
    avg_vel = sum(velocity_array) / len(velocity_array) if velocity_array else 0
    avg_ir = sum(ir_sig) / len(ir_sig) if ir_sig else 0
    avg_rad = sum(rad_sig) / len(rad_sig) if rad_sig else 0
    
    energy_discrepancy = (avg_vel**2) / (avg_ir + 1e-9)
    signature_mismatch = avg_rad > 0.5 and avg_ir < 0.1
    
    return bool(energy_discrepancy > 100.0 and signature_mismatch)

def visualize_track_and_predict(track_coords, lat_axis, lon_axis, t_axis, vel_axis=None, prediction_seconds=10, output_file="test_uap_map.html", auto_open=True):
    if len(track_coords) < 2: return
    
    t_vals = [t_axis[t_idx] for t_idx, _, _ in track_coords]
    lats = [lat_axis[lat_idx] for _, lat_idx, _ in track_coords]
    lons = [lon_axis[lon_idx] for _, _, lon_idx in track_coords]
    
    dy_deg = lats[-1] - lats[-2]
    dx_deg = lons[-1] - lons[-2]
    dt = t_vals[-1] - t_vals[-2]
    if dt == 0: dt = 1e-9
    
    pred_lat = lats[-1] + (dy_deg / dt) * prediction_seconds
    pred_lon = lons[-1] + (dx_deg / dt) * prediction_seconds
    
    center_lat = sum(lats)/len(lats)
    center_lon = sum(lons)/len(lons)
    
    nodes_js = ""
    t_start = t_vals[0]
    for i, (lat, lon, t) in enumerate(zip(lats, lons, t_vals)):
        speed_str = ""
        if vel_axis and i < len(vel_axis):
            # API returns m/s. Convert to knots (1 m/s = 1.94384 knots)
            speed_knots = vel_axis[i] * 1.94384
            speed_str = f"<br>Speed: {speed_knots:.0f} knots"
            
        tooltip = f"<b>Time: +{t - t_start:.0f}s</b><br>Lat: {lat:.5f}<br>Lon: {lon:.5f}{speed_str}"
        nodes_js += f"L.circleMarker([{lat}, {lon}], {{color: 'darkred', fillColor: 'red', fillOpacity: 1, radius: 6}}).addTo(map).bindTooltip('{tooltip}');\n"
        
    track_pts = "[" + ",".join([f"[{lat},{lon}]" for lat, lon in zip(lats, lons)]) + "]"
    pred_pts = f"[[{lats[-1]}, {lons[-1]}], [{pred_lat}, {pred_lon}]]"
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>UAP Kinematic Track Map</title>
    <meta http-equiv="refresh" content="10">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.3/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.3/dist/leaflet.js"></script>
    <style> #map {{ width: 100vw; height: 100vh; margin: 0; padding: 0; }} body {{ margin: 0; padding: 0; }} </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([{center_lat}, {center_lon}], 4);
        L.tileLayer('https://tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap'
        }}).addTo(map);

        L.polyline({track_pts}, {{color: 'red', weight: 4}}).addTo(map).bindTooltip("Observed Flight Path");
        {nodes_js}
        L.polyline({pred_pts}, {{color: 'orange', weight: 4, dashArray: "10, 10"}}).addTo(map).bindTooltip("Predicted Trajectory (+{prediction_seconds}s)");
        L.marker([{pred_lat}, {pred_lon}]).addTo(map).bindTooltip("Extrapolated Position");
    </script>
</body>
</html>"""

    with open(output_file, "w") as f:
        f.write(html)
        
    print(f"Generated {output_file}!")
    
    # Auto-open in browser only if requested!
    if auto_open:
        try:
            webbrowser.open('file://' + os.path.realpath(output_file))
        except:
            pass


if __name__ == "__main__":
    lat_axis = [0.0, 5.0, 5.0]
    lon_axis = [0.0, 0.0, 5.0]
    t_axis = [0.0, 1.0, 2.0]

    track_coords = [
        [0, 0, 0],
        [1, 1, 1],
        [2, 2, 2]
    ]
    
    print("Is Anomalous?", evaluate_kinematic_track(track_coords, lat_axis, lon_axis, t_axis))
    visualize_track_and_predict(track_coords, lat_axis, lon_axis, t_axis, output_file="test_uap_map.html")
