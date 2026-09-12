from __future__ import annotations

import importlib.util
from pathlib import Path


DEPTH_ROOT = Path(__file__).parents[1]
GENERAL_ROOT = DEPTH_ROOT.parent / "book-to-skill"
TECHNICAL_ROOT = DEPTH_ROOT.parent / "technical-book-to-skill"


def _load_validator(root: Path):
    module_path = root / "tools" / "validate_anki_tsv.py"
    spec = importlib.util.spec_from_file_location("validate_anki_tsv", module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_depth_skill_documents_source_coverage_gate():
    text = (DEPTH_ROOT / "SKILL.md").read_text(encoding="utf-8")

    assert "Source-Coverage Pass" in text
    assert "coverage ledger" in text
    assert "whole-book omission check" in text
    assert "Do not invent" in text


def test_both_generators_document_feynman_anki_stage():
    for root in (GENERAL_ROOT, DEPTH_ROOT):
        text = (root / "SKILL.md").read_text(encoding="utf-8")
        assert "Stage 2" in text
        assert "Anki" in text
        assert "Feynman" in text
        assert "book-learning tutor" in text
        assert "TSV" in text
        assert "one idea per card" in text


def test_technical_variant_is_installed_and_defaults_to_technical():
    skill_path = TECHNICAL_ROOT / "SKILL.md"
    assert skill_path.is_file()
    text = skill_path.read_text(encoding="utf-8")

    assert "name: technical-book-to-skill" in text
    assert "technical books" in text.lower()
    assert "BOOK_TYPE=technical" in text
    assert "Stage 2" in text


def test_anki_validator_accepts_valid_deck_and_rejects_duplicate_fronts(tmp_path):
    validator = _load_validator(DEPTH_ROOT)
    valid = tmp_path / "valid.tsv"
    valid.write_text(
        "Front\tBack\tTags\n"
        "What is a habit loop?\tCue, craving, response, and reward.\tbook::ch01::concept\n"
        "When should I reduce friction?\tWhen I want to make a behavior easier to start.\tbook::ch02::application\n",
        encoding="utf-8",
    )
    assert validator.validate_deck(valid) == []

    invalid = tmp_path / "invalid.tsv"
    invalid.write_text(
        "Front\tBack\tTags\n"
        "What is a habit loop?\tAnswer one.\tbook::ch01::concept\n"
        "What is a habit loop?\tAnswer two.\tbook::ch01::concept\n",
        encoding="utf-8",
    )
    findings = validator.validate_deck(invalid)
    assert any("duplicate" in finding.lower() for finding in findings)
