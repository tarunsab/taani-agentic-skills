#!/usr/bin/env python3
"""Validate the portable TSV deck emitted by book-to-skill Stage 2."""

from __future__ import annotations

import csv
import sys
from pathlib import Path


EXPECTED_HEADER = ["Front", "Back", "Tags"]


def validate_deck(path: Path) -> list[str]:
    """Return all validation findings for an Anki TSV deck."""

    findings: list[str] = []
    if not path.is_file():
        return [f"Deck does not exist: {path}"]

    try:
        handle = path.open("r", encoding="utf-8", newline="")
    except UnicodeDecodeError as exc:
        return [f"Deck is not valid UTF-8: {exc}"]
    except OSError as exc:
        return [f"Could not read deck: {exc}"]

    with handle:
        reader = csv.reader(handle, delimiter="\t")
        try:
            header = next(reader)
        except StopIteration:
            return ["Deck is empty; expected a Front, Back, Tags header"]

        if header != EXPECTED_HEADER:
            findings.append(
                "Invalid header: expected 'Front\\tBack\\tTags' "
                f"but found {header!r}"
            )

        seen_fronts: dict[str, int] = {}
        for line_number, row in enumerate(reader, start=2):
            if len(row) != 3:
                findings.append(
                    f"Line {line_number}: expected 3 tab-separated fields, "
                    f"found {len(row)}"
                )
                continue

            front, back, tags = row
            if not front.strip():
                findings.append(f"Line {line_number}: Front is blank")
            if not back.strip():
                findings.append(f"Line {line_number}: Back is blank")
            if not tags.strip():
                findings.append(f"Line {line_number}: Tags are blank")
            elif any(char.isspace() for char in tags.split(" ") if char):
                findings.append(f"Line {line_number}: Tags contain whitespace inside a tag")

            normalized_front = " ".join(front.casefold().split())
            if normalized_front:
                previous_line = seen_fronts.get(normalized_front)
                if previous_line is not None:
                    findings.append(
                        f"Line {line_number}: duplicate Front; first seen on line "
                        f"{previous_line}"
                    )
                else:
                    seen_fronts[normalized_front] = line_number

            if "\n" in front or "\r" in front or "\n" in back or "\r" in back:
                findings.append(
                    f"Line {line_number}: Front and Back must stay on one physical TSV row; "
                    "use <br> for display line breaks"
                )

    return findings


def main(argv: list[str] | None = None) -> int:
    args = argv if argv is not None else sys.argv[1:]
    if len(args) != 1:
        print("Usage: validate_anki_tsv.py <deck.tsv>", file=sys.stderr)
        return 2

    path = Path(args[0])
    findings = validate_deck(path)
    if findings:
        print(f"INVALID: {path}")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print(f"VALID: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
