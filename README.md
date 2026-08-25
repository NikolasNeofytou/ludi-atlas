# Ludi · Limassol venue atlas

One page, one map, every Limassol pitch and where it stands in the pipeline.
Nikolas edits; Louka reads.

## Files
- `index.html` — the atlas (Leaflet + CARTO tiles, no build step, no keys)
- `venues.json` — the published data. The page fetches this first; if it is missing (e.g. opened from file://) it falls back to the copy embedded in index.html.

## Publish workflow (Nikolas only)
1. Open the page with `?edit` on the URL (editor mode sticks on that device).
2. Change stages / actions / log entries. Every save goes to a draft in the browser (amber bar).
   For a venue with no Google listing (an unregistered futsal), use the **Locate** field in the
   edit form: search a street/place (OpenStreetMap, no key) or press **Pick on map** and click.
3. Press **Export JSON** → `venues.json` downloads.
   (**Export PDF** — available to readers too — prints an offline pipeline brief:
   next steps first, then every venue by stage. A stage-chip filter narrows the brief
   to that stage. Choose "Save as PDF" in the dialog.)
   (**Plan** — also for readers — tap venues in the order you'll visit them; pins get
   numbered badges, and **Export plan PDF** prints just those stops in sequence.
   The plan is per-device and survives reloads; Clear resets it.)
4. Replace `venues.json` in the repo and push. GitHub Pages redeploys; Louka's link now shows the new state.
5. Press **Discard draft** so your browser reads the published file again.

## Deploy
Push this folder to a GitHub repo, enable Pages from the root of `main`. Share the plain URL with Louka; keep `?edit` to yourself.

## Data model (per venue)
`id, name, area, lat, lng, place_id, operator, phone, pitches, stage, owner, next_action, next_date, flags[], log[{date,text}]`

Stages: unqualified → contacted → visited → proposal → onboarding → live, or lost.
A pin gets a red ring when `next_date` is in the past and the venue is neither live nor lost.
