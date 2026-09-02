# Ludi · Cyprus venue atlas

One page, one map, every commercial pitch in Cyprus and where it stands in the
pipeline. Nikolas edits; Louka and Theophanis read. A district selector in the
panel scopes the list, the map, the counts, and the PDF brief (venues without a
district count as Limassol, the original patch).

## Files
- `index.html` — the atlas (Leaflet + CARTO tiles, no build step, no keys)
- `venues.json` — the published data. The page fetches this first; if it is missing (e.g. opened from file://) it falls back to the copy embedded in index.html. Keep the embedded copy in sync when editing the file by hand.

## Publish workflow (Nikolas only)
1. Open the page with `?edit` on the URL (editor mode sticks on that device).
2. Change stages / actions / log entries. Every save goes to a draft in the browser (amber bar).
   For a venue with no Google listing (an unregistered futsal), use the **Locate** field in the
   edit form: search a street/place (OpenStreetMap, no key) or press **Pick on map** and click.
3. Press **Export JSON** → `venues.json` downloads.
4. Replace `venues.json` in the repo and push. GitHub Pages redeploys; the readers' link shows the new state within ~10 minutes (Pages cache).
5. Press **Discard draft** so your browser reads the published file again.

## Reports and plans (all views)
- **Export PDF** prints an offline pipeline brief: next steps first, then every venue
  by stage. The district selector and stage-chip filter narrow the brief. Choose
  "Save as PDF" in the dialog.
- **Plan** — tap venues in the order you'll visit them; pins get numbered badges,
  **Export plan PDF** prints just those stops in sequence, and **Open route in Maps**
  builds turn-by-turn directions through them (first 10 stops). The plan is
  per-device and survives reloads; Clear resets it.

## Field crew loop (reader view — Louka & Theophanis)
- Tap "N on Louka" or "N on Theophanis" in the summary to see only that person's venues.
- Each venue's sheet has **Navigate** (turn-by-turn in Google Maps) and **Open in
  Maps** — built from the venue's coordinates, so they work for every venue, with
  or without a Google listing.
- Each venue's sheet has **Report back on WhatsApp** — a prefilled report (venue,
  stage, planned action, "what happened: …") they finish and send to Nikolas,
  who logs it and publishes.

## Deploy
Push this folder to a GitHub repo, enable Pages from the root of `main`. Share the plain URL with the field crew; keep `?edit` to yourself.

## Data model (per venue)
`id, name, area, district, lat, lng, place_id, operator, phone, pitches, stage, owner, next_action, next_date, flags[], log[{date,text}]`

Stages: unqualified → contacted → visited → proposal → onboarding → live, or lost.
A pin gets a red ring when `next_date` is in the past and the venue is neither live nor lost.

## Data provenance
Seeded from the desk research in the Ludi repo (`docs/ludi-*-supply-scan.md`):
Larnaca, Nicosia and Paphos on 2026-08-25, Famagusta on 2026-09-02. Coordinates
and phones are grade-B (platform-listed) unless a log line says otherwise, and
nothing is verified on site — treat every field as a hypothesis until the first
visit, per the scans themselves.

Famagusta is the thinnest district on the island: one commercial small-sided
court (Ballers Club), one municipal 11v11 camp complex, one unidentified sports
complex. Wembley Park sits in **Larnaca** district (Xylofagou) but is driven on
the Famagusta run — switch its district in the editor if you want it on the
Famagusta brief.
