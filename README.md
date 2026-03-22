# 🛸 Live UAP Tracker & Physics Engine

A state-of-the-art live radar tracking module and a zero-dependency mathematical physics engine capable of verifying high-G maneuvers, scraping live OpenSky API telemetry, and predicting interactive trajectory maps dynamically.

## 🚀 Features
- **Live Flight Pipeline:** Connects directly to the OpenSky Network API to grab live aircraft telemetry.
- **Pure Vector Kinematics:** A zero-dependency math engine ([uaps_found.py](cci:7://file:///e:/Gdrive...+/uap_analysis/uaps_found.py:0:0-0:0)) that analyzes pitch, velocity, and sharp vector turns to accurately measure G-forces in real time.
- **Dynamic Leaflet Mapping:** Automatically generates a live auto-refreshing HTML map (`live_uap_map.html`) showing exactly where the tracked object is and extrapolating its future trajectory.
- **Absolute Portability:** Uses 100% built-in Python libraries (`urllib`, `json`, `math`). No `pip install` required!

## ⚙️ How to Use
1. Clone this repository.
2. Run the tracker in your terminal:
   ```bash
   python live_flight_tracker.py
