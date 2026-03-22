import urllib.request
import json
import time

# Import our perfect zero-dependency physics engine and mapping tool!
from uaps_found import evaluate_kinematic_track, visualize_track_and_predict

# Sweeping the skies over California/Western US
BBOX = "lamin=32.5&lomin=-124.5&lamax=42.0&lomax=-114.1"
API_URL = f"https://opensky-network.org/api/states/all?{BBOX}"

def get_live_flights():
    try:
        req = urllib.request.Request(API_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            return data.get('states', [])
    except Exception as e:
        print(f"API Error: {e}")
        return None

def track_live_aircraft(poll_interval=10):
    print("============== LIVE CONTINUOUS UAP/RADAR TRACKER ==============")
    print("Initiating Live Radar Scrape over Western United States...")
    
    history = {}  # type: dict
    target_icao = None
    
    # Phase 1: Hunt for an extremely fast flying aircraft
    while not target_icao:
        print(f"Fetching airspace data pulse at {time.strftime('%H:%M:%S')}...")
        states = get_live_flights()
        current_time = time.time()
        
        if states:
            for state in states:
                icao24 = state[0]
                callsign = str(state[1]).strip()
                lon = state[5]
                lat = state[6]
                on_ground = state[8]
                velocity = state[9] 
                
                # We want something flying incredibly fast (>200 m/s) to track!
                if not on_ground and lat is not None and lon is not None and velocity is not None and velocity > 200:
                    target_icao = icao24
                    history[target_icao] = {'callsign': callsign, 't': [current_time], 'lat': [lat], 'lon': [lon], 'vel': [velocity]}
                    print(f"\n+++ LOCKED ONTO SECTOR TARGET! (Hex: {target_icao}, Callsign: '{callsign}') +++")
                    break
                    
        if not target_icao:
            print(f"Waiting {poll_interval} seconds for high-speed intercepts...")
            time.sleep(poll_interval)

    # Phase 2: Lock & Continuous Track
    print("\n--- CONTINUOUS TRACKING ENGAGED ---")
    print("The map will automatically refresh every 10 seconds tracking this target live!")
    print("Leave this terminal open to continue monitoring...\n")
    opened_browser_already = False
    
    while True:
        print(f"\n[Tracking {history[target_icao]['callsign']}] Polling telemetry at {time.strftime('%H:%M:%S')}...")
        states = get_live_flights()
        current_time = time.time()
        
        target_found_this_cycle = False
        if states:
            for state in states:
                if state[0] == target_icao:
                    lon = state[5]
                    lat = state[6]
                    velocity = state[9]
                    
                    if lat is not None and lon is not None:
                        history[target_icao]['t'].append(current_time)
                        history[target_icao]['lat'].append(lat)
                        history[target_icao]['lon'].append(lon)
                        history[target_icao]['vel'].append(velocity if velocity is not None else 0)
                        target_found_this_cycle = True
                    break
        
        if not target_found_this_cycle:
            print("WARNING: Target lost on this sweep or left area. Waiting for re-acquisition...")
            
        data = history[target_icao]
        lat_axis = data['lat']
        lon_axis = data['lon']
        t_axis = data['t']
        vel_axis = data['vel']
        
        track_coords = [[i, i, i] for i in range(len(t_axis))]
        
        print(f"Total ping sequence stored: {len(t_axis)} live vectors.")
        
        # We need at least 3 positional dots to form two distinct vectors for differential physics
        if len(t_axis) >= 3:
            is_anomalous = evaluate_kinematic_track(track_coords, lat_axis, lon_axis, t_axis)
            if is_anomalous:
                 print("!!! ALERT: KINEMATIC ANOMALY DETECTED IN LIVE TRACK! OVER G-FORCE LIMITS !!!")
            else:
                 print("Validation: Standard Newtonian physics confirmed. No anomalies.")
                 
            # Overwrite the HTML actively. It will tell the Browser to only pop up the window ONCE, 
            # and then under the hood it just silently overwrites the HTML while your browser natively refreshes!
            visualize_track_and_predict(
                track_coords, 
                lat_axis, 
                lon_axis, 
                t_axis, 
                vel_axis=vel_axis,
                prediction_seconds=60, 
                output_file="live_uap_map.html", 
                auto_open=not opened_browser_already
            )
            opened_browser_already = True
            
        time.sleep(poll_interval)

if __name__ == "__main__":
    track_live_aircraft(poll_interval=10)
