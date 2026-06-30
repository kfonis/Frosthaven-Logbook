# Agent Instructions

## Project Purpose

This repository is a Frosthaven campaign journal for the party Kulturministeriet. It is written as a Markdown-based GitHub Pages site with illustrated session entries.

## Important Files

- `index.md`: homepage, quick links, active party, current story threads, and recent entries.
- `Logbook.md`: main campaign chronicle.
- `PartyRoster.md`: character descriptions, retired characters, personalities, and recurring jokes.
- `template.md`: structure for new session notes and logbook entries.
- `sources/Classes.md`: class lore and flavor reference.
- `sources/class-sheets.pdf`: playable class sheets; use as background for class identity and as the visual likeness reference for character illustrations.
- `sources/`: Frosthaven reference PDFs and supporting material.
- `sources/extracted/`: local, ignored flavor-text extracts of the source PDFs when present.
- `assets/images/`: generated or saved images used by the logbook.

## How To Work

- Preserve the existing Markdown-first structure.
- Keep edits focused on the requested journal, roster, image, or navigation change.
- Use `template.md` as the starting structure for new session entries.
- Update `index.md` whenever the latest session, active party, retired characters, or current story threads change.
- Update `PartyRoster.md` when a character joins, retires, changes class state, or gains important recurring characterization.
- Add new images under `assets/images/` and reference them with relative paths.
- Follow the existing image filename pattern: `logbook-week-###-scenario-name.png`.
- Do not rewrite old campaign history unless explicitly asked.
- Do not introduce spoilers beyond what is already present in the repository or provided by the user.
- When writing characters in play, use `sources/Classes.md` for class lore and `sources/class-sheets.pdf` for class-sheet context and visual identity.
- When generating new logbook images, draw each character's species, silhouette, clothing, weapons, equipment, and class motifs from `sources/class-sheets.pdf`, then adapt them to the named character's established personality and table jokes.
- When source-book flavor is needed, prefer `sources/extracted/` if it exists because it is faster and more searchable than the PDFs.
- Do not use extracted files as a gameplay rules reference; gameplay setup and mechanics are intentionally filtered out.
- Preserve and follow `Referenced sections` metadata when tracing scenario and section chains.
- Prefer `sources/extracted/section-reference-graph.md` for transitive `read xy.z` section chains.
- Do not commit extracted source-book text.
- Prefer concise, vivid prose over exhaustive rules recaps.

## Tone

- Match the journal's voice: adventurous, slightly dramatic, and willing to make room for table jokes.
- Preserve character names, running jokes, and party-specific wording.
- Keep rules details clear but secondary to the story of the session.

## Verification

- Check Markdown links after adding or renaming sections.
- Confirm that image paths used in Markdown exist.
- Confirm that new week anchors match the links from `index.md`.
- Avoid changing generated source files, PDFs, or unrelated campaign notes unless the user asks.
