from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path

import fitz


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCENARIO_PDF = ROOT / "sources" / "scenario-book.pdf"
DEFAULT_SECTION_PDF = ROOT / "sources" / "section book.pdf"
DEFAULT_OUTPUT_DIR = ROOT / "sources" / "extracted"

SCENARIO_TITLE_RE = re.compile(r"^\s*(\d{1,3})(?:\s+(CONT\.))?\s*\u2022\s*(.+?)\s*$")
SCENARIO_TRAILING_NUMBER_RE = re.compile(r"^\s*(.+?)\s+(\d{1,3})\s*\u2022\s*((?:[A-Z]\d{1,2})|FR)\s*$")
SECTION_TITLE_RE = re.compile(r"\b(\d{1,3}\.\d)\s*\u2022\s*([^\n\r]+)")
READ_REF_RE = re.compile(r"\bread\s+(\d{1,3}\.\d)\b", re.IGNORECASE)
LOOSE_READ_REF_RE = re.compile(r"\bread\b(?:(?!\b\d{1,3}\.\d\b).){0,1200}\b(\d{1,3}\.\d)\b", re.IGNORECASE | re.DOTALL)
GAMEPLAY_LABELS = {
    "Boss Special 1",
    "Boss Special 2",
    "Conclusion",
    "Loot",
    "Map Layout",
    "Rewards",
    "Scenario Goals",
    "Scenario Key",
    "Section Links",
    "Special Rules",
}
NON_FLAVOR_PREFIXES = (
    "Add event ",
    "Add ",
    "All City Guards ",
    "All Algox ",
    "All enemies ",
    "All monsters ",
    "At the start ",
    "At the end ",
    "Boss Special ",
    "Do not ",
    "Each ",
    "For a more ",
    "Gain ",
    "If any ",
    "If Glowing Catacombs ",
    "If Temple of Liberation ",
    "It is normal ",
    "Locked Out Scenario",
    "Open all doors ",
    "Place ",
    "Pebbles rain down ",
    "Set up ",
    "Switches ",
    "The Collector performs",
    "The first time ",
    "The scenario is complete ",
    "When door ",
    "When any door ",
    "You should now be ready ",
)
NON_FLAVOR_TERMS = (
    "ability deck",
    "boss special",
    "character summon",
    "characters have escaped",
    "elite for",
    "goal treasure tile",
    "hazardous terrain",
    "hit point",
    "initiative",
    "loot token",
    "monster ability",
    "Border hex",
    "is an ally to you",
    "perform an Outpost Phase",
    "spawn one",
    "spawn two",
    "suffer damage",
    "suffers damage",
)
MAP_OR_COUNTER_RE = re.compile(
    r"^(?:"
    r"\d+|"
    r"[A-Z]|"
    r"x\d+|"
    r"\d{2}-[A-Z]|"
    r"\d+-hex.*|"
    r".*\b(?:Door|Corridor|Debris|Trap|Treasure|Altar|Sarcophagus|Pillar|Rock|Snowdrift|Stalagmites|Tile|Wall|Obstacle|Pressure Plate|Ice)\b"
    r")$",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class Scenario:
    number: int
    location: str
    title: str
    page_index: int
    page_number: int
    y0: float
    continuation: bool = False


@dataclass(frozen=True)
class Section:
    section_id: str
    title: str
    page_number: int


@dataclass(frozen=True)
class TextBlock:
    column: int
    y0: float
    x0: float
    text: str


@dataclass(frozen=True)
class SectionEntry:
    section_id: str
    heading: TextBlock
    blocks: list[TextBlock]


@dataclass(frozen=True)
class SectionMetadata:
    entry: SectionEntry
    labels: list[str]
    refs: list[str]


def slugify(value: str, fallback: str = "untitled") -> str:
    value = value.lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = value.strip("-")
    return value or fallback


def clean_block(text: str, page_number: int | None = None) -> str:
    text = text.replace("\u00a0", " ")
    lines: list[str] = []

    for raw_line in text.splitlines():
        line = " ".join(raw_line.split()).strip()
        if not line:
            continue
        if page_number is not None and line == str(page_number):
            continue
        if "CEPHALOFAIR GAMES" in line and "RIGHTS RESERVED" in line:
            continue
        lines.append(line)

    return "\n".join(lines)


def is_layout_or_counter_line(line: str) -> bool:
    return bool(MAP_OR_COUNTER_RE.match(line.strip()))


def is_gameplay_block(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    if not lines:
        return True

    compact = " ".join(lines)
    if SECTION_TITLE_RE.search(compact):
        return False

    if compact in GAMEPLAY_LABELS:
        return True

    if any(compact.startswith(prefix) for prefix in NON_FLAVOR_PREFIXES):
        return True

    lower = compact.lower()
    if any(term.lower() in lower for term in NON_FLAVOR_TERMS):
        return True

    alpha_count = sum(1 for char in compact if char.isalpha())
    symbol_count = sum(1 for char in compact if char in "+-:,()")
    if symbol_count > alpha_count:
        return True

    has_sentence_punctuation = any(char in compact for char in ".?!\"\u201d")
    if len(compact) <= 80 and not has_sentence_punctuation:
        return True

    layout_line_count = sum(1 for line in lines if is_layout_or_counter_line(line))
    if layout_line_count == len(lines):
        return True

    # Scenario setup lists are often mostly counters, monsters, tiles, or map labels.
    if len(lines) > 1 and layout_line_count / len(lines) >= 0.6:
        return True

    return False


def column_centers(x_positions: list[float]) -> list[float]:
    if not x_positions:
        return [0.0]

    clusters: list[list[float]] = []
    for x_position in sorted(x_positions):
        if not clusters or x_position - clusters[-1][-1] > 80:
            clusters.append([x_position])
        else:
            clusters[-1].append(x_position)

    return [sum(cluster) / len(cluster) for cluster in clusters]


def nearest_column(centers: list[float], x0: float) -> int:
    return min(range(len(centers)), key=lambda index: abs(centers[index] - x0))


def section_sort_key(section_id: str) -> list[int]:
    return [int(part) for part in section_id.split(".")]


def extract_text_blocks(
    page: fitz.Page,
    page_number: int,
    flavor_only: bool = False,
    layout_columns: bool = False,
) -> list[TextBlock]:
    raw_blocks: list[tuple[float, float, str]] = []
    for block in page.get_text("blocks"):
        x0, y0, x1, y1, text = block[:5]
        cleaned = clean_block(text, page_number)
        if flavor_only and is_gameplay_block(cleaned):
            continue
        if cleaned:
            heading_lines = [line for line in cleaned.splitlines() if SECTION_TITLE_RE.search(line)]
            if layout_columns and len(heading_lines) > 1 and len(heading_lines) == len(cleaned.splitlines()):
                for line in heading_lines:
                    section_id = SECTION_TITLE_RE.search(line).group(1)  # type: ignore[union-attr]
                    rects = [
                        rect
                        for rect in page.search_for(section_id)
                        if x0 - 2 <= rect.x0 <= x1 + 2 and y0 - 2 <= rect.y0 <= y1 + 2
                    ]
                    rect = rects[0] if rects else fitz.Rect(x0, y0, x0, y0)
                    raw_blocks.append((rect.x0, rect.y0, line))
                continue

            label_lines = [line for line in cleaned.splitlines() if line.strip() in GAMEPLAY_LABELS]
            if layout_columns and len(label_lines) > 1 and len(label_lines) == len(cleaned.splitlines()):
                for line in label_lines:
                    label = line.strip()
                    rects = [
                        rect
                        for rect in page.search_for(label)
                        if x0 - 2 <= rect.x0 <= x1 + 2 and y0 - 2 <= rect.y0 <= y1 + 2
                    ]
                    rect = rects[0] if rects else fitz.Rect(x0, y0, x0, y0)
                    raw_blocks.append((rect.x0, rect.y0, label))
                continue

            raw_blocks.append((x0, y0, cleaned))

    centers = column_centers([x0 for x0, _y0, _text in raw_blocks]) if layout_columns else [0.0]
    blocks = [
        TextBlock(
            column=nearest_column(centers, x0) if layout_columns else 0,
            y0=y0,
            x0=x0,
            text=cleaned,
        )
        for x0, y0, cleaned in raw_blocks
    ]

    return blocks


def page_blocks(page: fitz.Page, page_number: int, flavor_only: bool = False) -> list[str]:
    blocks = extract_text_blocks(page, page_number, flavor_only=flavor_only, layout_columns=flavor_only)
    return [block.text for block in sorted(blocks, key=lambda block: (block.column, block.y0, block.x0))]


def block_is_after_heading(block: TextBlock, heading: TextBlock) -> bool:
    if block.column < heading.column:
        return False
    if block.column == heading.column:
        return block.y0 > heading.y0
    return True


def block_is_before_next_heading(block: TextBlock, heading: TextBlock, next_heading: TextBlock | None) -> bool:
    if next_heading is None:
        return True

    if next_heading.column == heading.column:
        return block.y0 < next_heading.y0

    if block.column < next_heading.column:
        return True

    if block.column == next_heading.column and block.y0 >= next_heading.y0:
        return False

    return block.column <= next_heading.column


def section_entries(page: fitz.Page, page_number: int, flavor_only: bool) -> list[SectionEntry]:
    blocks = extract_text_blocks(page, page_number, flavor_only=flavor_only, layout_columns=True)
    headings: list[tuple[str, TextBlock]] = []

    for block in blocks:
        match = SECTION_TITLE_RE.search(block.text)
        if match:
            headings.append((match.group(1), block))

    if not headings:
        return []

    headings = sorted(headings, key=lambda item: section_sort_key(item[0]))
    heading_blocks = {id(block) for _section_id, block in headings}
    headings_by_column: dict[int, list[tuple[str, TextBlock]]] = {}
    for section_id, heading in headings:
        headings_by_column.setdefault(heading.column, []).append((section_id, heading))
    for column_headings in headings_by_column.values():
        column_headings.sort(key=lambda item: item[1].y0)

    assigned_by_section: dict[str, list[TextBlock]] = {section_id: [] for section_id, _heading in headings}

    def section_for_block(block: TextBlock) -> str | None:
        same_column = [
            (section_id, heading)
            for section_id, heading in headings_by_column.get(block.column, [])
            if heading.y0 < block.y0
        ]
        if same_column:
            return same_column[-1][0]

        previous_column_headings = [
            (section_id, heading)
            for section_id, heading in headings
            if heading.column < block.column and heading.y0 < block.y0
        ]
        if previous_column_headings:
            return max(
                previous_column_headings,
                key=lambda item: (item[1].column, item[1].y0, section_sort_key(item[0])),
            )[0]

        return None

    for block in blocks:
        block_id = id(block)
        if block_id in heading_blocks:
            continue

        section_id = section_for_block(block)
        if section_id is None:
            continue

        assigned_by_section[section_id].append(block)

    return [
        SectionEntry(
            section_id=section_id,
            heading=heading,
            blocks=sorted(assigned_by_section[section_id], key=lambda block: (block.column, block.y0, block.x0)),
        )
        for section_id, heading in headings
    ]


def section_page_blocks(page: fitz.Page, page_number: int) -> list[str]:
    entries = section_entries(page, page_number, flavor_only=True)
    if not entries:
        blocks = extract_text_blocks(page, page_number, flavor_only=True, layout_columns=True)
        return [block.text for block in sorted(blocks, key=lambda block: (block.column, block.y0, block.x0))]

    raw_refs = {
        entry.section_id: read_refs("\n\n".join(block.text for block in entry.blocks))
        for entry in section_entries(page, page_number, flavor_only=False)
    }

    output: list[str] = []
    for entry in entries:
        refs = raw_refs.get(entry.section_id, [])
        output.append(entry.heading.text)
        output.append(f"- Direct references: {', '.join(refs) if refs else 'None found'}")
        output.extend(block.text for block in entry.blocks)

    return output


def section_metadata(page: fitz.Page, page_number: int) -> list[SectionMetadata]:
    raw_entries = section_entries(page, page_number, flavor_only=False)
    raw_blocks = extract_text_blocks(page, page_number, flavor_only=False, layout_columns=True)
    label_blocks = [
        block
        for block in raw_blocks
        if any(line.strip() in GAMEPLAY_LABELS for line in block.text.splitlines())
    ]

    metadata: list[SectionMetadata] = []
    for entry in raw_entries:
        labels: list[str] = []
        for label_block in label_blocks:
            same_column_heading = label_block.column == entry.heading.column and label_block.y0 > entry.heading.y0
            preceding_label = label_block.column == entry.heading.column and label_block.y0 < entry.heading.y0
            if not (same_column_heading or preceding_label):
                continue

            for line in label_block.text.splitlines():
                label = line.strip()
                if label in GAMEPLAY_LABELS and label not in labels:
                    labels.append(label)

        refs = read_refs("\n\n".join(block.text for block in entry.blocks))
        metadata.append(SectionMetadata(entry=entry, labels=labels, refs=refs))

    return metadata


def page_text(page: fitz.Page, page_number: int, flavor_only: bool = False, section_aware: bool = False) -> str:
    if section_aware:
        return "\n\n".join(section_page_blocks(page, page_number))
    return "\n\n".join(page_blocks(page, page_number, flavor_only=flavor_only))


def page_markdown(
    book_title: str,
    page: fitz.Page,
    page_number: int,
    flavor_only: bool = False,
    keep_references: bool = True,
    section_aware: bool = False,
) -> str:
    body = page_text(page, page_number, flavor_only=flavor_only, section_aware=section_aware)
    metadata: list[str] = []
    if keep_references:
        refs = read_refs(page_text(page, page_number, flavor_only=False))
        metadata.append(f"- Referenced sections: {', '.join(refs) if refs else 'None found'}")

    metadata_text = "\n".join(metadata)
    if metadata_text:
        return f"# {book_title} - Page {page_number:03d}\n\n{metadata_text}\n\n{body}\n"

    return f"# {book_title} - Page {page_number:03d}\n\n{body}\n"


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def find_scenarios_on_page(page: fitz.Page, page_index: int) -> list[Scenario]:
    page_number = page_index + 1
    scenarios: list[Scenario] = []

    for block in page.get_text("blocks"):
        x0, y0, _x1, _y1, text = block[:5]
        if y0 > 730:
            continue

        flat = " ".join(clean_block(text, page_number).split())
        match = SCENARIO_TITLE_RE.match(flat)
        trailing_match = SCENARIO_TRAILING_NUMBER_RE.match(flat)

        if match:
            number = int(match.group(1))
            continuation = bool(match.group(2))
            remainder = match.group(3).strip()
            parts = remainder.split()

            location = ""
            title = remainder
            if not continuation and parts and re.match(r"^(?:[A-Z]\d{1,2}|FR)$", parts[0]):
                location = parts[0]
                title = " ".join(parts[1:]).strip() or remainder
        elif trailing_match:
            title = trailing_match.group(1).strip()
            number = int(trailing_match.group(2))
            location = trailing_match.group(3)
            continuation = False
        else:
            continue

        scenarios.append(
            Scenario(
                number=number,
                location=location,
                title=title,
                page_index=page_index,
                page_number=page_number,
                y0=y0,
                continuation=continuation,
            )
        )

    return sorted(scenarios, key=lambda item: (item.page_index, item.y0, item.number))


def find_sections_on_page(page: fitz.Page, page_number: int) -> list[Section]:
    text = page.get_text()
    sections: list[Section] = []
    seen: set[str] = set()

    for match in SECTION_TITLE_RE.finditer(text):
        section_id = match.group(1)
        if section_id in seen:
            continue

        title = " ".join(match.group(2).split()).strip()
        sections.append(Section(section_id=section_id, title=title, page_number=page_number))
        seen.add(section_id)

    return sections


def read_refs(text: str) -> list[str]:
    refs = set(READ_REF_RE.findall(text))
    refs.update(LOOSE_READ_REF_RE.findall(text))
    return sorted(refs, key=lambda item: [int(part) for part in item.split(".")])


def reachable_refs(start: str, graph: dict[str, list[str]]) -> list[str]:
    seen: set[str] = set()
    pending = list(graph.get(start, []))

    while pending:
        section_id = pending.pop(0)
        if section_id in seen:
            continue

        seen.add(section_id)
        pending.extend(ref for ref in graph.get(section_id, []) if ref not in seen)

    return sorted(seen, key=section_sort_key)


def write_section_reference_graph(
    output_dir: Path,
    section_refs: dict[str, list[str]],
    section_labels: dict[str, list[str]],
) -> None:
    lines = [
        "# Section Reference Graph",
        "",
        "Direct references are extracted from `read xy.z` text in each section.",
        "`Reachable references` follows those links transitively so section chains can be traced.",
        "",
        "| Section | Labels | Direct references | Reachable references |",
        "| --- | --- | --- | --- |",
    ]

    for section_id in sorted(section_refs, key=section_sort_key):
        direct = section_refs.get(section_id, [])
        reachable = reachable_refs(section_id, section_refs)
        lines.append(
            "| "
            + " | ".join(
                [
                    section_id,
                    ", ".join(section_labels.get(section_id, [])),
                    ", ".join(direct) if direct else "",
                    ", ".join(reachable) if reachable else "",
                ]
            )
            + " |"
        )

    write_text(output_dir / "section-reference-graph.md", "\n".join(lines) + "\n")


def extract_scenario_book(pdf_path: Path, output_dir: Path) -> list[Scenario]:
    doc = fitz.open(pdf_path)
    book_dir = output_dir / "scenario-pages"
    scenario_dir = output_dir / "scenarios"

    all_pages: list[str] = []
    scenario_headings: list[Scenario] = []

    for page_index, page in enumerate(doc):
        page_number = page_index + 1
        text = page_markdown("Scenario Book", page, page_number, flavor_only=True)
        page_path = book_dir / f"page-{page_number:03d}.md"
        write_text(page_path, text)
        all_pages.append(f"## Page {page_number:03d}\n\n{text.split('\n\n', 1)[1]}")

        scenario_headings.extend(find_scenarios_on_page(page, page_index))

    write_text(output_dir / "scenario-book.md", "# Scenario Book Extract\n\n" + "\n\n".join(all_pages))

    scenario_starts = [heading for heading in scenario_headings if not heading.continuation]
    continuation_pages: dict[int, set[int]] = {}
    for heading in scenario_headings:
        if heading.continuation:
            continuation_pages.setdefault(heading.number, set()).add(heading.page_index)

    index_lines = [
        "# Scenario Index",
        "",
        "| Scenario | Location | Title | Pages | File | Section refs |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for index, scenario in enumerate(scenario_starts):
        next_start = scenario_starts[index + 1].page_index if index + 1 < len(scenario_starts) else doc.page_count
        page_indices = sorted(set(range(scenario.page_index, next_start)) | continuation_pages.get(scenario.number, set()))
        if not page_indices:
            page_indices = [scenario.page_index]
        pages_label = ", ".join(str(page_index + 1) for page_index in page_indices)
        combined_text = "\n\n".join(page_text(doc[page_index], page_index + 1, flavor_only=False) for page_index in page_indices)
        refs = read_refs(combined_text)

        scenario_file = scenario_dir / f"scenario-{scenario.number:03d}-{slugify(scenario.title)}.md"
        scenario_md = [
            f"# Scenario {scenario.number:03d} - {scenario.title}",
            "",
            f"- Location: {scenario.location or 'Unknown'}",
            f"- Source pages: {pages_label}",
            f"- Referenced sections: {', '.join(refs) if refs else 'None found'}",
            "",
        ]

        for page_index in page_indices:
            page_number = page_index + 1
            scenario_md.append(f"## Source Page {page_number:03d}")
            scenario_md.append("")
            scenario_md.append(page_text(doc[page_index], page_number, flavor_only=True))
            scenario_md.append("")

        write_text(scenario_file, "\n".join(scenario_md))

        index_lines.append(
            "| "
            + " | ".join(
                [
                    str(scenario.number),
                    scenario.location or "",
                    scenario.title,
                    pages_label,
                    f"[{scenario_file.name}]({relative(scenario_file)})",
                    ", ".join(refs),
                ]
            )
            + " |"
        )

    write_text(output_dir / "scenario-index.md", "\n".join(index_lines) + "\n")
    return scenario_starts


def extract_section_book(pdf_path: Path, output_dir: Path) -> list[Section]:
    doc = fitz.open(pdf_path)
    book_dir = output_dir / "section-pages"

    all_pages: list[str] = []
    sections: list[Section] = []
    section_refs: dict[str, list[str]] = {}
    section_labels: dict[str, list[str]] = {}

    for page_index, page in enumerate(doc):
        page_number = page_index + 1
        text = page_markdown("Section Book", page, page_number, flavor_only=True, section_aware=True)
        page_path = book_dir / f"page-{page_number:03d}.md"
        write_text(page_path, text)
        all_pages.append(f"## Page {page_number:03d}\n\n{text.split('\n\n', 1)[1]}")
        sections.extend(find_sections_on_page(page, page_number))

        for metadata in section_metadata(page, page_number):
            section_refs[metadata.entry.section_id] = metadata.refs
            section_labels[metadata.entry.section_id] = metadata.labels

    write_text(output_dir / "section-book.md", "# Section Book Extract\n\n" + "\n\n".join(all_pages))

    index_lines = [
        "# Section Index",
        "",
        "The section book uses dense multi-column layouts. Use this index to jump to the",
        "page containing a section, then read that page file for the exact extracted text.",
        "",
        "| Section | Title | Page | Labels | Direct refs | Page file |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    for section in sorted(sections, key=lambda item: [int(part) for part in item.section_id.split(".")]):
        page_file = output_dir / "section-pages" / f"page-{section.page_number:03d}.md"
        refs = section_refs.get(section.section_id, [])
        labels = section_labels.get(section.section_id, [])
        index_lines.append(
            "| "
            + " | ".join(
                [
                    section.section_id,
                    section.title,
                    str(section.page_number),
                    ", ".join(labels),
                    ", ".join(refs),
                    f"[page-{section.page_number:03d}.md]({relative(page_file)})",
                ]
            )
            + " |"
        )

    write_text(output_dir / "section-index.md", "\n".join(index_lines) + "\n")
    write_section_reference_graph(output_dir, section_refs, section_labels)
    return sections


def write_readme(output_dir: Path, scenario_count: int, section_count: int) -> None:
    readme = f"""# Extracted Frosthaven Sources

Generated local flavor-text extracts for fast private searching. Gameplay setup,
map layout, combat rules, rewards, and similar mechanics are filtered out, while
section references are retained as metadata.

- Scenarios found: {scenario_count}
- Sections found: {section_count}

Useful files:

- `scenario-index.md`: scenario number, title, source pages, and referenced sections.
- `section-index.md`: section number, source page, labels, and direct references.
- `section-reference-graph.md`: labels plus direct and transitive section reference chains.
- `scenario-book.md`: flavor-only page-by-page scenario book extract with section references.
- `section-book.md`: flavor-only page-by-page section book extract with section references.
- `scenarios/`: one generated file per scenario, including continuation pages.
- `scenario-pages/` and `section-pages/`: one generated file per PDF page.

These files are ignored by Git through `.gitignore` because they contain source
book text.
"""
    write_text(output_dir / "README.md", readme)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract local Frosthaven PDF sources to searchable Markdown.")
    parser.add_argument("--scenario-pdf", type=Path, default=DEFAULT_SCENARIO_PDF)
    parser.add_argument("--section-pdf", type=Path, default=DEFAULT_SECTION_PDF)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    scenarios = extract_scenario_book(args.scenario_pdf, output_dir)
    sections = extract_section_book(args.section_pdf, output_dir)
    write_readme(output_dir, scenario_count=len(scenarios), section_count=len(sections))

    print(f"Wrote extracted sources to {relative(output_dir)}")
    print(f"Scenarios found: {len(scenarios)}")
    print(f"Sections found: {len(sections)}")


if __name__ == "__main__":
    main()
