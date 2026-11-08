# 📘 OrbitDB Step-by-Step Guide — For Non-Tech Professionals

**You need zero coding experience.** Follow the numbers. Everything takes ~10 minutes total.
**You only need:** a web browser + one free API key + one AI app (Claude Desktop / Cursor / VS Code / ChatGPT).

---

## What is OrbitDB? (30-second version)

- A **search engine for space data** — like Google, but only for NASA, ESA, JAXA, ISRO… data.
- An **API Playground** — try a real NASA API without writing code.
- An **MCP Builder** — turns the data into a plug-in for your AI app, so the AI answers with *real live data* instead of guessing.

## What is an MCP server? (plain English)

Think of it as a **USB cable between your AI app and NASA data**.
- You plug the server in → your AI can suddenly *fetch real Mars photos, asteroid tracks, solar flares…*
- You write **one config file** with your file path. That's it.

---

## STEP 1 — Open OrbitDB (1 minute)

1. Find the file `index.html` in your Downloads / project folder.
2. **Double-click it.** It opens in your browser (Chrome/Safari/Firefox/Edge).
3. You should see a dark space-themed page with a big search box: *“Try: Mars rover photos…”*
4. ✅ If you see that, you're ready.

> **Tip:** You can also drag `index.html` into an open browser window.

## STEP 2 — Search in plain English (2 minutes)

1. Click the big search box (or press `/`).
2. Type something natural — **not** a file name, a sentence:
   - `Mars rover photos`
   - `asteroids near Earth`
   - `water on Earth from space`
   - `sun solar flare`
3. Click **Search** (or Enter). Watch the **🧠 Semantic expansion** line under the results — that's the app understanding your words (e.g. “red planet” → Mars).
4. Every result card tells you **Why this matched** — read that before trusting it.
5. Use the left sidebar to narrow down: tick **Agency** (NASA, ESA…), **Theme** (Mars, Climate…), **Format**.

**Try this:** search `climate` → tick agency `NASA` → sort by **Popularity** → open **NASA Climate Data & Portal**.

## STEP 3 — Open a dataset & try its API (2 minutes)

1. Click any card (or its **Details** button) — a panel slides in from the right with:
   - What it is, who publishes it, license, last updated
   - The live **endpoint URL**
   - **Sample request** (what you send) + **Sample response** (what you get back)
   - MCP tools it provides
2. Click **▶ Try live API**. A window opens:
   - Pick the endpoint (it's pre-selected)
   - Fill any parameters (e.g. `start_date = 2026-11-08`)
   - Leave the **API key** as `DEMO_KEY` for trying
   - Click **▶ Run request**
   - Watch the right side fill with real JSON data.
3. Change a parameter (e.g. a different date) → **Run** again. **You just used a real NASA API.**
4. **📋 Copy** the URL or **⬇ JSON** to save it.

> **If you see “CORS blocked / sample shown”** — that's normal for some endpoints in a browser. Don't worry: the **MCP server** runs outside the browser and always gets live data. Continue to Step 5.

## STEP 4 — Get your free NASA API key (1 minute) — read this first

### What is an API key? (plain English)

Every time your MCP server asks NASA for data, it must send a **key** — like a library card that says “this is me”. NASA lets you make **1,000 requests/hour** with your own key.

### DEMO_KEY vs. your free key

| | 🆓 `DEMO_KEY` (default in OrbitDB) | ✅ Your free key |
|---|---|---|
| **Limit** | **30 requests/hour** (shared, per IP) | **1,000 requests/hour** (yours alone) |
| **What 1 request is** | 1× ▶ Run in Playground **or** 1× AI tool call | same |
| **When it breaks** | After ~10 AI questions you’ll see `429 Too Many Requests` | you’d need ~30× more questions |
| **Cost** | $0 | $0, free forever, no card |

> **That’s what “Using DEMO_KEY — get a free key for 1,000 req/hr” means in the Builder:** nothing is broken. It’s OrbitDB telling you “you’re on the 30/hr demo; 1 minute of signup gets you 33× more.” You can ignore it for a first test — you’ll just hit the wall sooner.

### Where to get it (exact clicks)

1. Open **[https://api.nasa.gov/index.html#browse-api](https://api.nasa.gov/index.html#browse-api)**
2. Click **Generate API Key** (top of page; says **Sign Up** on some layouts)
3. Enter your **email** + a one-line purpose (e.g. `OrbitDB MCP experiments`) → **Submit**
4. Check your inbox (~1 min; check **Spam/Junk** if missing) → **copy the key** from the email (looks like `aBc123XyZ…`)
5. Save it in your password manager / notes. Paste it in **two places** in OrbitDB:
   - **▶ API Playground** — replace `DEMO_KEY` in the API key field
   - **⚡ MCP Builder → Step 5** — paste into the API key box → it’s baked into your downloaded server + config
6. In your AI app’s config, it appears as `NASA_API_KEY` in `env` — **don’t commit that file to public GitHub** (it’s not a password, but it’s yours; revoke + regenerate if leaked).

> **Is it safe?** Yes. NASA API keys only rate-limit data requests — not a password, not payment info. Free forever. If you skip it, nothing breaks — you just get `30/hr` and a `429` when you exceed it. Wait 1 minute (limit resets hourly) or paste your key and re-run.

## STEP 5 — Install Python (one-time, 2 minutes)

> Skip this if you already have Python or Node. Python is easiest for beginners.

1. Go to **[python.org/downloads](https://www.python.org/downloads/)** → click the big yellow **Download Python**.
2. Run the installer. ⚠️ **On the very first screen, tick “Add python.exe to PATH”** (bottom-left, easy to miss!). Then **Install Now**.
3. Open **Terminal** (Mac: Cmd+Space → `Terminal`) or **Command Prompt** (Windows: Win+R → `cmd`).
4. Type this and press Enter:
   ```
   pip install mcp httpx
   ```
   Wait for it to finish (about 30–60 seconds). No red errors = success.

**Prefer Node?** Go to [nodejs.org](https://nodejs.org) → install the LTS version → then in Terminal:
```
npm i @modelcontextprotocol/sdk zod
```

## STEP 6 — Create your MCP server in the Builder (1 minute)

1. Scroll down to **“⚡ One-Click MCP Server Builder”** on the OrbitDB page.
2. **Click the dataset buttons** you want (they turn purple when selected). Start with the default 6.
3. Choose:
   - **Language:** `🐍 Python` (recommended)
   - **Transport:** `📟 stdio` (your app is on the same computer — most people)
   - **Your AI app:** `Claude Desktop` / `Cursor` / `VS Code` / `OpenCode` / `Generic`
4. Paste your **NASA API key** into the box (or leave blank for `DEMO_KEY`).
5. Click **⬇ Download full bundle** — this gives you one text file with *everything*: server code + config + install + test prompts. (Or **⬇ Download file** for just the server.)
6. Save it somewhere permanent like `Documents/space-mcp/space_mcp.py`.

> **Important:** Remember that exact folder path — you'll need it in Step 7. Example: `/Users/yourname/Documents/space-mcp/space_mcp.py` (Mac) or `C:\Users\you\Documents\space-mcp\space_mcp.py` (Windows).

## STEP 7 — Connect your AI app (2 minutes)

### Claude Desktop
1. In the Builder, click the **⚙️ App config** tab → **📋 Copy**.
2. Open Claude Desktop → **Settings** → **Developer** (or **MCP**).
3. Open the config file path shown in the copied text:
   - Mac: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
4. Paste the JSON, **replace `python` args path** (`/ABSOLUTE/PATH/space_mcp.py`) with *your real path* from Step 6. Save.
5. **Fully quit and reopen** Claude Desktop (not just close the window).

### Cursor
1. Copy the **App config** tab from the Builder.
2. In Cursor: **Settings** (gear icon) → **MCP** → **Add new server** → paste → fix the path → **Save**. Restart Cursor.

### VS Code (with GitHub Copilot / MCP extension)
1. Copy the **App config** tab.
2. Create a file `.vscode/mcp.json` in your project → paste → fix the path → save → **Start** the server.

### OpenCode
1. Copy the **App config** tab → paste the `mcp` block into `opencode.json` → fix the path → restart OpenCode.

### ChatGPT / n8n / anything else
1. In the Builder choose **Transport: 🌐 Streamable HTTP** (instead of stdio).
2. Run the server with the `--http` flag (see Install tab).
3. Point your app at `http://localhost:8000/mcp`.

## STEP 8 — Test it! 🎉 (1 minute)

1. In your AI app's chat, click the **🔌 MCP / tools** icon and confirm you see tools like `get_apod`, `get_mars_photos`, `get_asteroids_this_week`.
2. Copy-paste a **Test prompt** from the Builder's **🧪 Test prompts** tab, e.g.:
   > *Use `get_asteroids_this_week` for 2026-11-08 to 2026-11-14 and show the 5 closest with size and velocity.*
3. ✅ **Success looks like:** the AI calls the tool, shows a table/list with real numbers + names + dates, and cites the data source. Not vague “in general…”.
4. Try the follow-up: *“Now explain that in 5 bullets for a 10-year-old, keep numbers exact.”*

## SAMPLE INPUT → OUTPUT (what to expect)

| # | You type (to your AI) | MCP tool called | You get back |
|---|---|---|---|
| 1 | *"Picture of the day from 1 Nov 2026"* | `get_apod` | `{ "date": "2026-11-01", "title": "Andromeda Over the Alps", "explanation": "…", "url": "…jpg" }` |
| 2 | *"Mars photos, sol 1000"* | `get_mars_photos` | `{ "photos": [{ "id": 154, "sol": 1000, "camera": {"name": "FHAZ"}, "img_src": "…jpg", "earth_date": "2015-05-30" }] }` |
| 3 | *"Asteroids this week, closest 5"* | `get_asteroids_this_week` | `{ "element_count": 3, "near_earth_objects": { "2026-11-08": [{ "name": "(2024 XA12)", "estimated_diameter": {"meters": {"estimated_diameter_min": 68}}, "close_approach_data": [{"miss_distance": {"kilometers": "1240000"}}] }] } }` |
| 4 | *"Solar flares 1–7 Nov 2026"* | `get_solar_flares` | `[{ "flrID": "2026-11-03…", "classType": "M4.2", "sourceLocation": "S12E40" }]` |
| 5 | *"Where is the ISS right now?"* | `get_iss_position` | `{ "name": "ISS (ZARYA)", "latitude": 12.4, "longitude": -84.2, "altitude": 412.5, "velocity": 7.66 }` |
| 6 | *"Biggest exoplanets?"* | `query_exoplanets` | `[{ "pl_name": "K2-18 b", "pl_eqt": 265, "pl_rade": 2.61 }]` |

> The AI app will reformat the JSON into a friendly table or paragraph — the **numbers come from the real API**, not the AI's memory.

## WORKED EXAMPLE — 5-minute full journey

1. Search **`asteroids near Earth`** → open **Near Earth Object Web Service** → read the endpoint + sample.
2. **▶ Try API** → `start_date=2026-11-08`, `end_date=2026-11-14` → **Run** → live JSON appears.
3. Get your key at **api.nasa.gov** (Step 4).
4. **MCP Builder**: select *Near Earth Objects* + *APOD* + *Mars Photos* → client **Claude Desktop** → paste key → **⬇ Download full bundle**.
5. Install Python + `pip install mcp httpx` (Step 5) → save server as `space_mcp.py`.
6. Paste config into Claude Desktop (Step 7) → restart Claude → ask: *"Any asteroids passing Earth this week? Show the closest 3."* 🎉

## TROUBLESHOOTING

| Problem | Fix |
|---|---|
| **“DEMO_KEY” / 429 error** | Rate limit hit. Paste your own free key (Step 4). Wait 1 minute. |
| **“Server not found” in your AI app** | Path is wrong. Use the **absolute** path (starts with `/Users/…` or `C:\…`). No `~`, no relative paths. |
| **AI app shows no tools** | Fully quit + reopen the app. Check the config JSON is valid (paste it into [jsonlint.com](https://jsonlint.com) to verify). |
| **Server window / terminal shows nothing** | Normal for stdio! No output = waiting for your AI app. Press `Ctrl+C` to stop. |
| **`pip` / `node` not found** | Re-run the installer and tick **“Add to PATH”** (Python) / restart Terminal after Node install. |
| **Playground shows sample, not live** | Browser CORS blocking. Use the MCP server (Step 7) or open the URL in a new tab — that always works. |
| **“I don't know what an API is”** | An API is just a **URL that returns data**. The Playground builds that URL for you. You never type API syntax — you type English into your AI. |

## GLOSSARY

- **API (Application Programming Interface):** a URL that returns structured data (JSON).
- **MCP (Model Context Protocol):** the standard “plug” that lets AI apps call tools like the ones above.
- **Tool:** a function the AI can call, e.g. `get_apod`.
- **stdio:** the server talks to your app through Terminal (same computer).
- **HTTP:** the server listens on a web address (`localhost:8000`) so remote apps can reach it.
- **Endpoint:** the URL of a dataset's API.
- **Sol:** one Martian day (24.6 hours) — Mars rover photos are indexed by sol.

## NEXT STEPS

- Export your search (**⤓ JSON / CSV**) for your own spreadsheets or reports.
- Add more datasets in the Builder, re-download, and restart your AI app.
- Browse `data/catalog.json` and `examples/` in the repo for every endpoint and config.
