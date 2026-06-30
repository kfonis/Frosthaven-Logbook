# Workflow

## Add A New Session

1. Copy the structure from `template.md`.
2. Replace the placeholder week number and scenario name.
3. Fill in scenario number, date played, and characters present.
4. Record the quick outcome first.
5. Add session highlights and character moments.
6. Add funny quotes or table banter if available.
7. Add image notes if an illustration should be generated.
8. Turn the notes into a polished entry in `Logbook.md`.
9. Save or generate the session image in `assets/images/`.
10. Add the image reference to the new logbook entry.
11. Update `index.md` so the latest-entry block under Quick Links, its linked image, and the corresponding Current Story Threads recap and related-entry links are current. Remove any `Active Side Quests` subsection whose flowchart path has no visible outgoing scenarios left.
12. Update `PartyRoster.md` if character status, personality, retirement, or party composition changed.

## Convert Source Books

The Frosthaven scenario and section books are easier to use after converting them
to local searchable Markdown. The generated extracts keep flavor text and filter
out gameplay setup, map layout, combat rules, rewards, and similar mechanics.
Section references are retained as metadata so scenario and section chains can
still be followed. The extracted text is ignored by Git because it contains
source-book material.

Initial setup:

```powershell
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r tools\requirements.txt
```

Run the conversion:

```powershell
.venv\Scripts\python.exe tools\extract_frosthaven_sources.py
```

Generated files appear in `sources/extracted/`.

Use:

- `sources/extracted/scenario-index.md` to find a scenario file and its referenced sections.
- `sources/extracted/section-index.md` to find which section-book page contains a referenced section.
- `sources/extracted/section-reference-graph.md` to follow `read xy.z` chains across sections.
- `sources/extracted/scenarios/` for one generated flavor-text file per scenario.
- `sources/extracted/section-pages/` for page-level flavor-text section-book extracts.

## Update The Homepage

When adding a new session, check these sections in `index.md`:

- Quick Links
- Active Party
- Retired Adventurers
- Current Story Threads
- Latest-entry block and linked image under Quick Links

Recent journal links should point to the corresponding heading anchors in `Logbook.md`.

For Current Story Threads, place Algox, Lurker, and Unfettered scenarios under `Main Quest`. Place other active threads under `Active Side Quests`. When a new session advances a side quest, check `sources/scenario-flowchart.md`: if the played scenario has no visible outgoing scenarios left for that thread, remove that side quest from `Active Side Quests` instead of leaving it as active. Otherwise, briefly update that thread's recap and add the new logbook entry to its related-entry list.

## Add Or Update An Image

1. Choose a descriptive filename using the existing pattern.
2. Use `sources/class-sheets.pdf` as the visual reference for featured playable characters, matching class silhouette, ancestry, gear, weapons, and motifs while preserving the campaign character's own personality and recurring jokes.
3. Save it in `assets/images/`.
4. Reference it with a relative Markdown path.
5. Confirm the file exists and the path matches exactly.

Example:

```md
![Week 017: Scenario Name](assets/images/logbook-week-017-scenario-name.png)
```

## Update Party Information

Update `PartyRoster.md` when:

- A new character joins.
- A character retires.
- A character levels up in a way the journal tracks.
- A character gains a notable personality trait, recurring joke, title, or relationship.
- A retired character becomes relevant again.

Also update `index.md` if the active or retired party tables change.

## Quality Check

Before finishing a change:

- Confirm all Markdown links are valid.
- Confirm image paths exist.
- Confirm the latest week appears in `index.md` if applicable.
- Confirm `Active Side Quests` contains only threads that still have visible outgoing scenarios in `sources/scenario-flowchart.md`.
- Confirm character names and class names match existing usage.
- Keep unrelated files unchanged.
