# 🔬 OrbitDB — Sample Input → Output (all tools)

Use these **verbatim in your AI chat** after connecting the MCP server (see GUIDE-NONTECH.md Step 8).
Each row: **You type → Tool called → MCP returns (JSON, AI reformats it).**

## How to read this

- **Input** = what you type to Claude / Cursor / ChatGPT / VS Code / OpenCode.
- **Tool** = the MCP tool the AI calls (you'll see this in the app's tool inspector).
- **Output** = the real API JSON (truncated for readability; live data will be longer).

---

### 1 · get_apod — Astronomy Picture of the Day
**Input:** `Get the Astronomy Picture of the Day for 1 Nov 2026 — title, explanation, and image URL.`
```json
{ "date": "2026-11-01", "title": "Andromeda Over the Alps",
  "explanation": "A bright spiral galaxy…", "media_type": "image",
  "url": "https://apod.nasa.gov/…jpg", "service_version": "v1" }
```

### 2 · get_asteroids_this_week — Near Earth Objects
**Input:** `Find asteroids passing near Earth 8–14 Nov 2026 and show the closest 5 with size and velocity.`
```json
{ "element_count": 3, "near_earth_objects": { "2026-11-08": [{
  "name": "(2024 XA12)",
  "estimated_diameter": {"meters": {"estimated_diameter_min": 68, "estimated_diameter_max": 105}},
  "close_approach_data": [{ "close_approach_date": "2026-11-08",
    "relative_velocity": {"kilometers_per_second": "12.4"},
    "miss_distance": {"kilometers": "1240000"} }],
  "is_potentially_hazardous_asteroid": false }] } }
```

### 3 · get_mars_photos — Mars Rover Photos
**Input:** `Show Curiosity photos from sol 1000 — camera, image URL, Earth date.`
```json
{ "photos": [{ "id": 154, "sol": 1000,
  "camera": {"id": 20, "name": "FHAZ", "full_name": "Front Hazard Avoidance Camera A"},
  "img_src": "http://mars.jpl.nasa.gov/…jpg", "earth_date": "2015-05-30",
  "rover": {"name": "Curiosity", "status": "active"} }] }
```

### 4 · get_epic_images — EPIC Earth
**Input:** `Get today's EPIC full-disc Earth images with captions.`
```json
[{ "identifier": "20261106", "caption": "spacecraft selfie…",
   "image": "epic_1b_20261106…", "date": "2026-11-06 00:34:00",
   "centroid_coordinates": {"lat": 5.2, "lon": 21.5} }]
```

### 5 · query_exoplanets — Exoplanet Archive (ADQL)
**Input:** `Show the 5 largest confirmed exoplanets (radius) with equilibrium temp.`
```json
[{ "pl_name": "K2-18 b", "pl_eqt": 265, "pl_rade": 2.61, "pl_orbsdep": 33, "pl_bmasse": 8.63 }]
```

### 6 · get_solar_flares / get_cmes / get_geomagnetic_storms — DONKI
**Input:** `Solar flares from 1–7 Nov 2026, class M and above.`
```json
[{ "flrID": "2026-11-03T…", "beginTime": "2026-11-03T02:12:00Z",
   "peakTime": "2026-11-03T02:34:00Z", "classType": "M4.2",
   "sourceLocation": "S12E40", "activeRegionNum": 14910 }]
```
**Input:** `Any coronal mass ejections 1–7 Nov 2026?`
```json
[{ "cmeID": "2026-11-02T…", "startTime": "2026-11-02T10:00:00Z",
   "speed": 612, "halfAngleWidth": 30, "earthImpact": {"isGlancing": true} }]
```

### 7 · search_nasa_media — NASA Image & Video Library
**Input:** `Search NASA images for "Artemis II crew" — 3 results with titles and dates.`
```json
{ "collection": { "metadata": {"total_hits": 2843},
  "items": [{ "data": [{ "title": "Artemis II crew", "nasa_id": "KSC-2024", "date_created": "2024-…", "description": "…" }] }] } }
```

### 8 · get_iss_position — ISS
**Input:** `Where is the ISS right now?`
```json
{ "name": "ISS (ZARYA)", "latitude": 12.4, "longitude": -84.2,
  "altitude": 412.5, "velocity": 7.66, "visibility": "eclipsed", "footprint": 4432.1 }
```

### 9 · get_active_fires — FIRMS (VIIRS)
**Input:** `Active fires in the US in the last day — count and 3 examples.`
```csv
country_code,latitude,longitude,brightness,scan,track,acq_time,satellite,confidence,version,date
US,38.2,-97.1,312.5,1.2,1.1,0130,NPP,78,6.1,2026-11-06
```

### 10 · query_gaia_stars — ESA Gaia (ADQL)
**Input:** `Show 5 nearby stars with parallax > 50 mas from Gaia DR3.`
```json
[{ "source_id": 6729976490128798224, "ra": 80.8942, "dec": -69.7563, "parallax": 768.13, "pmra": -548.06 }]
```

### 11 · search_copernicus_scenes — ESA Copernicus
**Input:** `Search Sentinel-2 scenes over the last week — 3 examples.`
```json
{ "feed": { "entry": [{ "title": "S2A_…", "summary": "Sentinel-2 MSI L1C …", "gml:Polygon": "…" }] } }
```

### 12 · lookup_small_body — JPL Small-Body
**Input:** `Look up asteroid 433 (Eros).`
```json
{ "object": {"fullname": "433 Eros", "des": "433"},
  "orbit": {"i": 10.8, "e": 0.22, "a": 1.45}, "approach_data": [] }
```

### 13 · search_space_data — generic semantic search
**Input:** `Search space data for "water on Earth from space".`
```
nasa-climate: NASA Climate Data & Portal (NASA)
nasa-epic: Earth Polychromatic Imaging Camera (EPIC) (NASA)
esa-copernicus: Copernicus Earth Observation (Sentinels) (ESA)
Use a specific tool: get_apod, get_mars_photos, …
```

---

## Cross-dataset example
**Input:** `Compare Mars rover photos (sol 1000) with Landsat Earth imagery from the same week — what do both tell us about water?`
**Tools called:** `get_mars_photos` + `search_space_data` (→ Landsat / Earthdata context)
**Expected:** AI grounds both sides in real data: riverbeds/ancient lake (Mars) vs current reservoirs/irrigation (Earth), with image links.

## Success checklist
- [ ] AI shows a tool call, not just text
- [ ] Numbers/dates/names look specific (not “in general”)
- [ ] Sources/endpoints cited at the end
- [ ] Follow-up questions keep using the same data
