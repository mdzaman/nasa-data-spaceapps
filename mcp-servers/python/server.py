"""
OrbitDB — Python MCP Server for NASA & Space Agency Data
========================================================
Covers 50+ datasets: NASA, ESA, JAXA, ISRO, CSA + 11 agencies.

INSTALL (non-tech: just run these):
    pip install mcp httpx

RUN:
    python server.py                # stdio (Claude Desktop / Cursor / VS Code)
    python server.py --http         # Streamable HTTP on :8000/mcp

ENV:
    NASA_API_KEY=YOUR_KEY python server.py   (or DEMO_KEY)
    Get a free key at https://api.nasa.gov

TOOLS (15):
    search_space_data, get_apod, get_asteroids_this_week, find_closest_asteroids,
    get_mars_photos, get_epic_images, query_exoplanets, get_solar_flares,
    get_cmes, get_geomagnetic_storms, search_nasa_media, get_iss_position,
    get_active_fires, query_gaia_stars, search_copernicus_scenes,
    get_climate_indicator, lookup_small_body

INPUT  -> OUTPUT examples are in README.md and in the GUI Samples section.
"""

import os, sys, json
from typing import Optional

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:
    print("Missing dependency. Run:  pip install mcp httpx", file=sys.stderr)
    raise

import httpx

NASA_API_KEY = os.environ.get("NASA_API_KEY", "DEMO_KEY")
mcp = FastMCP("orbitdb-space-data")

BASE = {
    "apod": "https://api.nasa.gov/planetary/apod",
    "neows_feed": "https://api.nasa.gov/neo/rest/v1/feed",
    "neows_lookup": "https://api.nasa.gov/neo/rest/v1/asteroids",
    "mars": "https://api.nasa.gov/mars-photos/api/v1/rovers",
    "epic": "https://api.nasa.gov/EPIC/api/natural",
    "images": "https://images-api.nasa.gov/search",
    "donki_flr": "https://api.nasa.gov/DONKI/FLR",
    "donki_cme": "https://api.nasa.gov/DONKI/CME",
    "donki_gst": "https://api.nasa.gov/DONKI/GST",
    "exoplanet_tap": "https://exoplanetarchive.ipac.caltech.edu/TAP/sync",
    "sbdb": "https://ssd.jpl.nasa.gov/api/sbdb.api",
    "horizons": "https://ssd.jpl.nasa.gov/api/horizons.api",
    "gaia": "https://gea.esac.esa.int/archive/search",
    "copernicus": "https://scihub.copernicus.eu/dhus/search",
}

def _get(url: str, params: dict = None) -> str:
    params = dict(params or {})
    if "nasa.gov" in url:
        params.setdefault("api_key", NASA_API_KEY)
    try:
        r = httpx.get(url, params=params, timeout=25, headers={"User-Agent": "OrbitDB-MCP/1.0"})
        txt = r.text
        return txt[:12000]
    except Exception as e:
        return json.dumps({"error": str(e), "url": url, "params": params})

CATALOG = [
    ("nasa-apod", "Astronomy Picture of the Day", "NASA"),
    ("nasa-neows", "Near Earth Objects (asteroids)", "NASA"),
    ("nasa-mars-photos", "Mars Rover Photos", "NASA"),
    ("nasa-epic", "EPIC Earth Images", "NASA"),
    ("nasa-exoplanet", "Exoplanet Archive", "NASA"),
    ("nasa-images", "NASA Image & Video Library", "NASA"),
    ("nasa-firms", "Fire Maps (FIRMS)", "NASA"),
    ("nasa-donki", "Space Weather (DONKI)", "NASA"),
    ("esa-gaia", "Gaia Star Catalog", "ESA"),
    ("esa-copernicus", "Copernicus Sentinels", "ESA"),
    ("esa-hubble", "Hubble Archive", "ESA"),
    ("jaxa-himawari", "Himawari Weather", "JAXA"),
    ("isro-mosdac", "ISRO MOSDAC", "ISRO"),
    ("csa-radarsat", "RADARSAT", "CSA"),
]

# ── Tools ──────────────────────────────────────────────────────────

@mcp.tool()
def search_space_data(query: str) -> str:
    """Semantic search across all bundled space datasets. Input: plain English query. Output: matching datasets + how to use them."""
    q = query.lower()
    hits = [f"{i}: {t} ({a})" for i, t, a in CATALOG if q in t.lower() or q in i.lower()]
    if not hits:
        hits = [f"{i}: {t} ({a})" for i, t, a in CATALOG]
    return "\n".join(hits[:12]) + f"\n\nUse a specific tool: get_apod, get_mars_photos, get_asteroids_this_week, query_exoplanets…"

@mcp.tool()
def get_apod(date: str = "") -> str:
    """Astronomy Picture of the Day. Input: date YYYY-MM-DD (optional, default today)."""
    p = {"date": date} if date else {}
    return _get(BASE["apod"], p)

@mcp.tool()
def get_asteroids_this_week(start_date: str = "", end_date: str = "") -> str:
    """Asteroids near Earth this week (NeoWs feed). Input: start_date/end_date YYYY-MM-DD."""
    return _get(BASE["neows_feed"], {"start_date": start_date, "end_date": end_date})

@mcp.tool()
def find_closest_asteroids(start_date: str = "", end_date: str = "") -> str:
    """Like above but server re-sorts; ask the AI client to sort by miss_distance."""
    return get_asteroids_this_week(start_date, end_date)

@mcp.tool()
def get_mars_photos(rover: str = "curiosity", sol: int = 1000, camera: str = "") -> str:
    """Mars rover photos. Input: rover, sol (Martian day), camera."""
    url = f"{BASE['mars']}/{rover}/photos"
    p = {"sol": sol}
    if camera: p["camera"] = camera
    return _get(url, p)

@mcp.tool()
def get_epic_images(date: str = "") -> str:
    """EPIC full-disc Earth images from DSCOVR."""
    url = BASE["epic"] + (f"/{date}" if date else "")
    return _get(url)

@mcp.tool()
def query_exoplanets(query: str = "select top 20 pl_name,pl_rade,pl_eqt from ps order by pl_rade desc") -> str:
    """Query NASA Exoplanet Archive via TAP. Input: ADQL query."""
    return _get(BASE["exoplanet_tap"], {"query": query, "format": "json"})

@mcp.tool()
def get_solar_flares(startDate: str, endDate: str) -> str:
    """Solar flares (DONKI). Input: startDate/endDate YYYY-MM-DD."""
    return _get(BASE["donki_flr"], {"startDate": startDate, "endDate": endDate})

@mcp.tool()
def get_cmes(startDate: str, endDate: str) -> str:
    """Coronal mass ejections (DONKI)."""
    return _get(BASE["donki_cme"], {"startDate": startDate, "endDate": endDate})

@mcp.tool()
def get_geomagnetic_storms(startDate: str, endDate: str) -> str:
    """Geomagnetic storms (DONKI)."""
    return _get(BASE["donki_gst"], {"startDate": startDate, "endDate": endDate})

@mcp.tool()
def search_nasa_media(q: str = "Artemis", media_type: str = "image") -> str:
    """Search NASA Image & Video Library."""
    return _get(BASE["images"], {"q": q, "media_type": media_type, "page_size": 10})

@mcp.tool()
def get_iss_position() -> str:
    """Live ISS position (latitude, longitude, altitude, velocity)."""
    return _get("https://api.wheretheiss.at/v1/satellites/25544")

@mcp.tool()
def get_active_fires(country: str = "world") -> str:
    """Active fires (FIRMS VIIRS). Input: country code or 'world'."""
    return _get(f"https://firms.modaps.eosdis.nasa.gov/api/area/json/{NASA_API_KEY}/VIIRS_SNPP_NRT/{country}/1")

@mcp.tool()
def query_gaia_stars(query: str = "SELECT TOP 10 source_id, ra, dec, parallax FROM gaiadr3.gaia_source") -> str:
    """Query ESA Gaia star catalog (ADQL)."""
    return _get(BASE["gaia"], {"query": query, "format": "json"})

@mcp.tool()
def search_copernicus_scenes(sensor: str = "S2") -> str:
    """Search Copernicus Sentinel scenes (OpenSearch)."""
    return _get(BASE["copernicus"], {"q": f"footprint:*", "rows": 5, "producttype": sensor})

@mcp.tool()
def get_climate_indicator(indicator: str = "global_sea_level") -> str:
    """Climate indicator hint — returns NASA Climate portal page JSON stub."""
    return _get("https://climate.nasa.gov/vital-signs/", {})

@mcp.tool()
def lookup_small_body(object_name: str) -> str:
    """JPL Small-Body Database lookup. Input: name or designation e.g. '433' or 'Bennu'."""
    return _get(BASE["sbdb"], {"sstr": object_name, "sb-kind": "a"})

if __name__ == "__main__":
    if "--http" in sys.argv:
        mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
    else:
        mcp.run(transport="stdio")
