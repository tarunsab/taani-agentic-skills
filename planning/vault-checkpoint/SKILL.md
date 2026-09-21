---
name: vault-checkpoint
description: Run a comprehensive Obsidian vault health, link integrity, frontmatter schema, and structural audit. Operates in read-only mode by default, diagnosing broken links, orphans, duplicate notes, unreferenced attachments, configuration drift, and data loss risks, producing Vault Health Report.md, Vault Health Findings.json, and Vault Repair Manifest.md.
---

# Vault Checkpoint (Obsidian Vault Health & Integrity Audit)

Perform a comprehensive health check, static analysis, link audit, metadata schema inventory, and structural integrity audit of an Obsidian vault. 

This skill acts as a combination of:
- `fsck` for a Markdown filesystem
- Database integrity checking
- Static analysis for a knowledge codebase
- Dependency and broken link checking
- Information architecture review
- Obsidian best-practice and configuration audit

The goal is **not** to redesign the vault according to personal preferences, but to determine objectively what is broken, inconsistent, missing, duplicated, poorly connected, structurally unhealthy, at risk of silent failure, and what should deliberately be left alone.

---

## 1. Safety Rules & Four-Tier Boundaries

### Default Mode: Strictly Read-Only

During an audit:
- **DO NOT** delete, rename, move, or merge notes.
- **DO NOT** rewrite note content, modify frontmatter, or alter tags.
- **DO NOT** automatically repair links or remove attachments.
- **DO NOT** edit `.obsidian` configurations or change Git history.

**Protocol**: First inspect. Then report. Then propose fixes. Any destructive, lossy, difficult-to-reverse, or large-scale change requires explicit human approval.

### Four-Tier Storage Discipline

```text
TIER 1: EPHEMERAL LOCAL COMPUTATION
$HOME/.taani-agent/workspaces/ or local scratch
→ Python scripts, JSON dumps, parse caches, intermediate graph analysis.
→ Strictly OUTSIDE the Obsidian vault and iCloud.

TIER 2: PERSISTENT AI WORKING KNOWLEDGE
11 - Agents/Workspace/ (or dedicated Audit subfolder)
→ Human-readable non-canonical analysis, audit history, decision context.

TIER 3: CANONICAL VAULT TRUTH & DELIVERABLES
Vault Root / Designated Areas
→ Vault Health Report.md, Vault Health Findings.json, Vault Repair Manifest.md.
→ Requires explicit human approval before applying any repairs.

TIER 4: REUSABLE METHODOLOGY & TOOLING
~/.codex/skills/planning/vault-checkpoint/
→ Git-controlled, generic audit skill, tests, and CLI runner. Free of personal vault data.
```

---

## 2. Understand the Vault Before Judging It

Before flagging issues, inspect the vault sufficiently to infer its intended architecture:
- **Structure**: Johnny Decimal, PARA, or hybrid (e.g. `01 - Home`, `02 - Journal`, `02 - Taani`, `03 - Projects`, `04 - Areas`, `05 - Knowledge`, `06 - Resources`, `08 - Attachments`, `09 - Templates`, `10 - Archive`, `11 - Agents`).
- **Boundaries**: Shared vs private folders, Git-tracked vs nested Git repositories (e.g. local-only Finance repo).
- **Conventions**: Infer conventions from existing notes. Mark uncertain items as `NEEDS HUMAN REVIEW` rather than assuming.

---

## 3. The 36 Diagnostic Dimensions

1. **Safety Enforcement**: Strictly read-only audit mode.
2. **Architecture Understanding**: Identify intended folder boundaries and conventions.
3. **Filesystem Health**:
   - Illegal characters (`<`, `>`, `:`, `"`, `|`, `?`, `*`), leading/trailing spaces, accidental double spaces.
   - Case-only collisions, filename length risks.
   - Zero-byte files, temporary files (`.tmp`, `.bak`), sync conflict copies (`(1)`, `copy`, `conflict`).
4. **Markdown Integrity**:
   - Heading hierarchy jumps (e.g. `H1` directly to `H3`), malformed headings.
   - Unclosed code fences (odd count of ` ``` `).
   - Corrupt frontmatter, unclosed YAML blocks, duplicate YAML delimiters.
   - Git conflict remnants (`<<<<<<< HEAD`, `=======`, `>>>>>>>`).
5. **Wikilink & Link Integrity**:
   - Evaluate `[[WikiLinks]]`, `[[Page#Heading]]`, `[[Page^block-id]]`, `![[Embeds]]`, `[Markdown](links)`.
   - Broken internal links, broken embeds, stale renamed targets.
   - Ambiguous targets matching multiple files (e.g. identical filenames in different folders).
   - Classify confidence: `HIGH`, `MEDIUM`, `LOW`.
6. **Orphan Notes**:
   - Isolated notes (0 incoming, 0 outgoing).
   - Notes with no inbound links.
   - Distinguish legitimate standalone notes (reference docs, receipts, archive, book notes) from forgotten notes or navigation failures.
7. **Dead-End & Weakly Connected Notes**:
   - Notes with inbound links but no outgoing links.
   - MOCs and index notes that fail to link to active child notes.
8. **Duplicate & Near-Duplicate Content**:
   - Exact title matches across folders (collision hazards).
   - High text-similarity notes (distinguishing legitimate template derivatives from divergent copies).
9. **Frontmatter / Properties Health**:
   - Complete inventory of property keys and data types.
   - Schema fragmentation (e.g. `created` vs `date` vs `created_at`).
   - Missing required properties (e.g. `parent` or `tags`).
10. **Tag Taxonomy Health**:
    - Complete tag inventory (frontmatter and inline `#tag`).
    - Case variations, singular/plural variants, singletons (used only once).
    - Unresolved template placeholders leaking into tags (e.g. `#{{topic-tag}}`).
11. **Icon Health**:
    - Cross-check every path in `.obsidian/plugins/obsidian-icon-folder/data.json` against filesystem.
    - Stale mapped paths for moved/deleted files.
    - Folders or index notes missing icon declarations.
12. **Attachment Health**:
    - Check all files in `08 - Attachments/`.
    - Unreferenced attachments vs referenced missing attachments.
    - Unsupported file formats or oversized files.
13. **Structured Data Integrity**:
    - Validate JSON, YAML, CSV, TSV, and Obsidian `.base` files for syntax and referential integrity.
14. **Canonical vs Generated Data**:
    - Distinguish source of truth from AI-generated workspaces, caches, or snapshots.
15. **Automation & Path Portability**:
    - Hardcoded machine paths (e.g. absolute user home paths instead of relative or `$HOME`).
    - Stale scripts or workflow references.
16. **Obsidian Configuration Health**:
    - Core plugins enabled without configuration files (e.g. `daily-notes` missing `daily-notes.json`).
    - Community plugins, themes, and snippets pointing to deleted assets.
17. **Dataview / Query Health**:
    - Queries returning empty results due to folder moves.
    - Queries omitting folders due to missing index notes.
18. **Template Health**:
    - Validate `09 - Templates/`.
    - Check for broken link references, unclosed placeholders, or schema drift.
19. **Navigation / Structural Health**:
    - MOC freshness, missing entry points, overly deep or empty hierarchies.
20. **Naming Convention Health**:
    - Inconsistent capitalization, prefixes, or dating formats.
21. **Date & Periodic Note Health**:
    - Daily/weekly/monthly notes continuity and destination folders.
22. **Shared / Private Boundary Health**:
    - Sensitive notes accidentally placed in shared areas.
23. **Git Health**:
    - Main vault git status: untracked moves, deleted files, uncommitted changes.
    - Nested repositories (e.g. `02 - Taani/Finance/.git`).
    - Active unmerged worktrees in volatile paths (e.g. `/private/tmp/`).
24. **Sync Health**:
    - iCloud limitations: POSIX symlinks pointing outside iCloud cannot sync to iOS/mobile.
25. **Empty & Stale Areas**:
    - Empty folders or abandoned project indexes.
26. **Data Loss Risks**:
    - Volatile worktrees, untracked folder moves, hardcoded paths.
27. **Health Scoring**:
    - Quantitative scoring across 12 areas (0–100 scale).
28. **Severity Classification**:
    - P0 (Data loss / corruption), P1 (Broken functionality), P2 (Integrity / structural), P3 (Hygiene / maintainability), P4 (Optional).
29. **Confidence Levels**:
    - Assign `HIGH`, `MEDIUM`, or `LOW` confidence to every suggested repair.
30. **Vault Health Report**: Produce `Vault Health Report.md`.
31. **Machine-Readable Findings**: Produce `Vault Health Findings.json`.
32. **Repair Manifest**: Produce `Vault Repair Manifest.md`.
33. **Audit Metrics Header**: Include exact counts for notes, links, orphans, tags, etc.
34. **Value-First Discipline**: Prioritize integrity over cosmetic uniformity.
35. **Clarity Principle**: Distinguish Broken, Inconsistent, Risky, Stale, and Suboptimal.
36. **Final Output**: Conclude with Top 10 Actions ranked by Impact, Risk Reduction, Effort, and Confidence.

---

## 4. Deliverables Contract

When run, `vault-checkpoint` produces three files in the target vault:

1. **`Vault Health Report.md`**:
   - Executive summary, Audit metrics table, Health scorecard.
   - Critical findings (P0/P1), Link integrity, Icon health, Orphan notes, Duplicate notes, Metadata, Tags, Attachments, Structured data, Automation, Configuration, Git/sync resilience.
   - Suggested 5-phase repair plan and Top 10 Actions.
2. **`Vault Health Findings.json`**:
   - Validated machine-readable JSON schema of all issues:
     ```json
     {
       "audit_version": "1.0",
       "vault_path": "...",
       "timestamp": "...",
       "summary": {},
       "issues": [
         {
           "id": "VH-001",
           "severity": "P0",
           "category": "git-risk",
           "path": "...",
           "description": "...",
           "suggested_action": "...",
           "confidence": "HIGH",
           "auto_fix_safe": false
         }
       ]
     }
     ```
3. **`Vault Repair Manifest.md`**:
   - Categorized into:
     - **Safe Automatic Repairs** (deterministic, zero risk).
     - **Approval-Required Repairs** (renaming, moves, staging Git changes, index creations).
     - **Human Judgment Required** (content merges, ambiguous links, architectural decisions).

---

## 5. Running the Audit CLI

```bash
python3 ~/.codex/skills/planning/vault-checkpoint/scripts/vault-audit.py \
  --vault "/path/to/vault" \
  --output "/path/to/vault"
```
