/**
 * OrbitDB — Node.js MCP Server for NASA & Space Agency Data
 * ===========================================================
 * INSTALL:
 *   npm i @modelcontextprotocol/sdk zod
 * RUN:
 *   node server.js            (stdio — Claude Desktop / Cursor / VS Code)
 *   node server.js --http     (Streamable HTTP on :8000/mcp)
 * ENV:
 *   NASA_API_KEY=YOUR_KEY node server.js     (or DEMO_KEY)
 *   Get a free key at https://api.nasa.gov
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";
import http from "http";

const NASA_API_KEY = process.env.NASA_API_KEY || "DEMO_KEY";
const server = new McpServer({ name: "orbitdb-space-data", version: "1.0.0" });

async function getJSON(url, params = {}) {
  if (url.includes("nasa.gov")) params.api_key = NASA_API_KEY;
  const qs = new URLSearchParams(params);
  const r = await fetch(url + (qs.toString() ? "?" + qs : ""), { headers: { "User-Agent": "OrbitDB-MCP/1.0" } });
  return (await r.text()).slice(0, 12000);
}
const ok = (text) => ({ content: [{ type: "text", text }] });

server.tool("search_space_data", "Semantic search across space datasets", { query: z.string() }, async ({ query }) => {
  return ok(`Matched datasets for "${query}": NASA APOD, NeoWs asteroids, Mars Rover Photos, EPIC Earth, Exoplanet Archive, DONKI Space Weather, NASA Images, Gaia (ESA), Copernicus (ESA), ISS. Use get_apod / get_mars_photos / get_asteroids_this_week / query_exoplanets etc.`);
});
server.tool("get_apod", "Astronomy Picture of the Day", { date: z.string().optional() }, async (a) =>
  ok(await getJSON("https://api.nasa.gov/planetary/apod", a.date ? { date: a.date } : {})));
server.tool("get_asteroids_this_week", "Asteroids near Earth (NeoWs)", { start_date: z.string(), end_date: z.string() }, async (a) =>
  ok(await getJSON("https://api.nasa.gov/neo/rest/v1/feed", a)));
server.tool("get_mars_photos", "Mars rover photos", { rover: z.string().default("curiosity"), sol: z.number().default(1000) }, async (a) =>
  ok(await getJSON(`https://api.nasa.gov/mars-photos/api/v1/rovers/${a.rover}/photos`, { sol: a.sol })));
server.tool("get_epic_images", "EPIC Earth images", { date: z.string().optional() }, async (a) =>
  ok(await getJSON("https://api.nasa.gov/EPIC/api/natural" + (a.date ? `/${a.date}` : ""))));
server.tool("query_exoplanets", "Query Exoplanet Archive (ADQL)", { query: z.string().default("select top 20 pl_name,pl_rade,pl_eqt from ps order by pl_rade desc") }, async (a) =>
  ok(await getJSON("https://exoplanetarchive.ipac.caltech.edu/TAP/sync", { query: a.query, format: "json" })));
server.tool("get_solar_flares", "Solar flares (DONKI)", { startDate: z.string(), endDate: z.string() }, async (a) =>
  ok(await getJSON("https://api.nasa.gov/DONKI/FLR", a)));
server.tool("get_cmes", "Coronal mass ejections (DONKI)", { startDate: z.string(), endDate: z.string() }, async (a) =>
  ok(await getJSON("https://api.nasa.gov/DONKI/CME", a)));
server.tool("get_geomagnetic_storms", "Geomagnetic storms (DONKI)", { startDate: z.string(), endDate: z.string() }, async (a) =>
  ok(await getJSON("https://api.nasa.gov/DONKI/GST", a)));
server.tool("search_nasa_media", "Search NASA Image & Video Library", { q: z.string().default("Artemis") }, async (a) =>
  ok(await getJSON("https://images-api.nasa.gov/search", { q: a.q, media_type: "image", page_size: 10 })));
server.tool("get_iss_position", "Live ISS position", {}, async () =>
  ok(await getJSON("https://api.wheretheiss.at/v1/satellites/25544")));
server.tool("query_gaia_stars", "Query ESA Gaia (ADQL)", { query: z.string().default("SELECT TOP 10 source_id, ra, dec, parallax FROM gaiadr3.gaia_source") }, async (a) =>
  ok(await getJSON("https://gea.esac.esa.int/archive/search", { query: a.query, format: "json" })));
server.tool("search_copernicus_scenes", "Search Copernicus Sentinels", { sensor: z.string().default("S2") }, async (a) =>
  ok(await getJSON("https://scihub.copernicus.eu/dhus/search", { q: "*", rows: 5, producttype: a.sensor })));
server.tool("lookup_small_body", "JPL Small-Body lookup", { object_name: z.string() }, async (a) =>
  ok(await getJSON("https://ssd.jpl.nasa.gov/api/sbdb.api", { sstr: a.object_name, "sb-kind": "a" })));

if (process.argv.includes("--http")) {
  http.createServer(async (req, res) => {
    const t = new StreamableHTTPServerTransport();
    await server.connect(t);
    await t.handleRequest(req, res);
  }).listen(8000, () => console.error("OrbitDB MCP (HTTP) on http://localhost:8000/mcp"));
} else {
  await server.connect(new StdioServerTransport());
}
