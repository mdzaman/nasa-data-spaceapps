# ☄️ OrbitDB — Semantic Space Data Portal

**One semantic search for NASA + ESA + JAXA + ISRO + CSA + 11 more agencies — with a one-click MCP server builder for any AI app.**

> Open `index.html` in any browser. No install, no server, no build. That's the whole app.

## ✨ What it does

| Feature | Detail |
|---|---|
| **Semantic search** | Plain English ("rover on red planet") → Mars Photos. Synonym graph (`SYNONYMS`), concept matching, ranked results with *Why this matched* explanations. Modes: Semantic / Keyword / Exact. |
| **Faceted catalog** | 50+ datasets · filters by agency, theme, format, date range · sort · Grid/List · favorites (persisted) · history · export **JSON/CSV** · **filter pills** (remove with ✕) |
| **Intuitive UX** | **Journey stepper** (6 steps, persisted) · **Welcome banner** · **“Best for…” + ✨ Start-here badges** on cards · **plain-English hints** everywhere · mobile menu · **❓ Help modal** · **Non-tech mode** in Builder · **presets** (Beginner/Earth/Deep Space/My search) |
| **Dataset detail** | 3-step drawer (What it is → Try it → Use in AI) + sticky actions + DCAT metadata, resources, sample I/O, related |
| **API Playground** | Live-run real endpoints. **Pre-filled examples** per field (date→today, sol→1000…), plain-English labels, “What am I seeing?” explainer, CORS fallback to sample + MCP tip. |
| **MCP Builder** | Progress bar (“Step X of 5”) + live summary (datasets/tools/key status) + validation warnings. Language + transport + client with **plain-English explanations** (stdio=“on this computer”). Complete runnable code + config + install + test prompts. |
| **Guide** | 6-step interactive checklist (persisted, with **📋 copy buttons** per step) + worked 5-minute example, inline |
| **Analytics** | Live counts by agency & theme (bar charts), stats header |
| **Keyboard / a11y** | `/` search · `Enter` run · `Esc` close · `↑↓` suggestions · skip-link · focus rings · reduced-motion |

## 🚀 Quick start (30 seconds)

1. Double-click `index.html` → it opens in your browser.
2. Search `asteroids near Earth` → open a card → **▶ Try API** → **Run**.
3. Scroll to **⚡ MCP Builder** → Download → paste config into your AI app.

> **API key?** `DEMO_KEY` = shared demo (**30 req/hr**) — good for a first test, exhausts after ~10 AI questions (`429`). Your **free key** = **1,000 req/hr**, 1 min at **[api.nasa.gov](https://api.nasa.gov/index.html#browse-api)** → *Generate API Key* → email. Paste it in Playground + Builder Step 5. See [GUIDE-NONTECH.md Step 4](GUIDE-NONTECH.md#step-4--get-your-free-nasa-api-key-1-minute--read-this-first) for screenshots-in-words.

## 🗂️ Repo layout

```
nasa-data-spaceapps/
├── index.html                  ← the entire GUI (self-contained)
├── README.md                   ← you are here
├── GUIDE-NONTECH.md            ← full step-by-step for non-tech professionals
├── data/catalog.json           ← dataset catalog (JSON, for ingestion)
├── examples/
│   ├── sample-input-output.md  ← sample I/O for every tool
│   └── claude_desktop_config.json / cursor_mcp.json / vscode_mcp.json / opencode.json
└── mcp-servers/
    ├── python/server.py        ← FastMCP server (15 tools)
    ├── python/requirements.txt
    └── node/server.js + package.json  ← MCP SDK server (14 tools)
```

## 🧩 MCP servers

**Python (recommended for non-tech)**
```bash
pip install mcp httpx
python mcp-servers/python/server.py            # stdio
python mcp-servers/python/server.py --http     # http://localhost:8000/mcp
```

**Node**
```bash
cd mcp-servers/node && npm i @modelcontextprotocol/sdk zod
node server.js            # stdio
node server.js --http     # http
```

**Config examples** — see `examples/` for ready-to-paste Claude Desktop / Cursor / VS Code / OpenCode configs. The GUI **MCP Builder** regenerates all of these with *your* dataset selection.

## 📊 Samples (short)

**Input (in Claude/Cursor/ChatGPT after setup):**
> Use `get_asteroids_this_week` for 2026-11-08 to 2026-11-14 and show the 5 closest with size & velocity.

**Output (MCP server returns JSON, AI formats it):**
```json
{ "element_count": 3,
  "near_earth_objects": {
    "2026-11-08": [{
      "name": "(2024 XA12)",
      "estimated_diameter": {"meters": {"estimated_diameter_min": 68, "estimated_diameter_max": 105}},
      "close_approach_data": [{
        "close_approach_date": "2026-11-08",
        "relative_velocity": {"kilometers_per_second": "12.4"},
        "miss_distance": {"kilometers": "1240000"}
      }],
      "is_potentially_hazardous_asteroid": false
    }]
  }
}
```
Full input/output table for all tools: `examples/sample-input-output.md`.

## 🔍 How semantic search works

1. **Expand** — query words → synonym groups (`mars` → rover, perseverance, sol, red planet…). See the expansion live under the search bar.
2. **Score** — title match ×3, concepts ×2.5, description ×1.5 + phrase boost + concept-overlap boost + popularity prior (rating, downloads).
3. **Explain** — every card shows *Why this matched* when you searched.

## 📚 Data sources

NASA (APOD, NeoWs, Mars Photos, EPIC, Exoplanet Archive, Images Library, FIRMS, DONKI, Landsat, GES DISC, NTRS, JPL Horizons/Small-Body/SPICE, ISS, SDO, ICESat-2, GRACE-FO, Earthdata…), ESA (Hubble, Gaia DR3, Copernicus Sentinels, Webb, Euclid, Planck, Solar Orbiter), JAXA (EORC, Himawari), ISRO (Bhuvan, MOSDAC), CSA (RADARSAT), CNSA, ASI, DLR, EUMETSAT, KARI, SANSA, AEB, UAE SA, SUPARCO.

For prototypes & education — always verify live data at source. NASA data: US Public Domain. Other agencies: per their open-data policies.

## ♿ Accessibility & ops

Single-file app, no cookies, no tracking, works offline after first load (beyond live API calls). Fonts via Google Fonts with system fallback.
