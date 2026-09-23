---
name: vault-sentry
description: Deep DFS directory-by-directory structural audit, link graph verification, note relocation recommendations, staleness/archival diagnosis, dual PARA conformance review, Iconize expected page icon auditing, and note destination suggestion routing for Obsidian vaults. Strictly read-only by default, producing Vault Health Report.md, Vault Health Findings.json, and Vault Repair Manifest.md.
---

# Vault Sentry

Perform an exhaustive, deep Depth-First Search (DFS) directory-by-directory structural audit, link graph verification, note relocation recommendation, staleness/archival diagnosis, dual PARA conformance review, Iconize coverage analysis, and note destination routing across an Obsidian vault.

`vault-sentry` acts as an automated knowledge architect and filesystem maintainer:
- **DFS Section-by-Section Structural Audit**: Traverses the vault directory tree in DFS order, evaluating folder health, index note presence, coherence of internal links, and flat folder overloading.
- **Dual PARA Conformance Review**: Rigorously assesses adherence to Tiago Forte's PARA framework at both the overall vault level (Projects, Areas, Resources, Archive) and within the shared household space (`02 - Taani`).
- **Iconize Coverage & Expected Page Icon Audit**: Verifies `.obsidian/plugins/obsidian-icon-folder/data.json` against all expected vault folders, indexes, book summaries, agent notes, and active content leaves, generating concrete icon suggestions (Lucide IDs and emojis).
- **Note Placement & Relocation ("Where it should live instead")**: Evaluates note contents against the Vault Constitution classification rules to identify misplaced notes and suggest clean, un-cluttered destinations.
- **Note Destination Routing Engine (`--suggest`)**: Suggests the optimal destination folder, clean filename, parent index wikilink, tags, icon, rationale, and frontmatter scaffold for any proposed new note or draft markdown file.
- **Staleness & Archival Sentry ("Suggest notes to archive")**: Detects outdated, untouched, superseded, or completed notes and proposes structured archival destinations under `10 - Archive/`.
- **Integrity & Safety**: Strictly read-only by default. Identifies broken links, sync collisions, Git hazards, and core plugin drift without mutating files until explicitly approved.

---

## 1. Safety Rules & Four-Tier Discipline

### Default Mode: Strictly Read-Only

During an audit:
- **DO NOT** delete, rename, move, or merge notes.
- **DO NOT** rewrite note content, modify frontmatter, or alter tags.
- **DO NOT** automatically repair links or remove attachments.
- **DO NOT** alter `.obsidian` configurations or change Git history.

**Protocol**: First inspect. Then report. Then stage proposed fixes in `Vault Repair Manifest.md`. All modifications require explicit user approval.

### Four-Tier Storage Architecture

```text
TIER 1: EPHEMERAL LOCAL COMPUTATION
$HOME/.taani-agent/workspaces/ or local scratch
→ Python scripts, JSON parse dumps, graph analysis.
→ Disposable, local-only, strictly OUTSIDE the vault / iCloud.

TIER 2: PERSISTENT AI WORKING KNOWLEDGE
11 - Agents/Workspace/
→ Durable, human-readable non-canonical AI analysis and reasoning.

TIER 3: CANONICAL VAULT TRUTH & AUDIT DELIVERABLES
11 - Agents/ (or Vault Root if unconfigured)
→ Vault Health Report.md, Vault Health Findings.json, Vault Repair Manifest.md, PARA Conformance Review.md, Iconize Coverage Audit.md.
→ Requires explicit human approval before applying any repairs.

TIER 4: REUSABLE METHODOLOGY & TOOLING
~/.codex/skills/planning/vault-sentry/
→ Git-controlled, generic audit skill, tests, and CLI runner. Free of personal vault data.
```

---

## 2. DFS Directory Traversal & Structural Sense

`vault-sentry` visits every directory in strict Depth-First Search (DFS) order and evaluates:

1. **Directory Depth & File Count**:
   - Flat directory overloading: Flags directories with $\ge 25$ notes without thematic subfolders (e.g. `02 - Taani/House` holding 48 flat notes across cleaning, appliances, renovation, and conveyancing).
2. **Entry Point / Index Note**:
   - Checks if the directory has a corresponding `00 - <Name> Index.md`.
   - Flags directories missing indexes (e.g. `04 - Areas/Technology`) which cause silent Dataview query omissions in parent indexes.
3. **Internal Link Coherence**:
   - Calculates the ratio of child notes that link to their parent index or vice versa.
   - Detects abandoned indexes with empty Dataview queries (e.g. `03 - Projects/00 - Projects Index.md`, `05 - Knowledge/Finance Index.md`).

---

## 3. Dual PARA Conformance Review

`vault-sentry` conducts a rigorous dual-layer analysis of PARA (Projects, Areas, Resources, Archive):

### Layer 1: Vault-Level PARA Conformance
- **Projects (`03 - Projects`)**: Must represent active, finite efforts with target completion conditions. Sentry audits whether `03 - Projects` has become depleted/dormant while active projects leak into other domains (e.g. trips in Travel, home improvements in House).
- **Areas (`04 - Areas`)**: Must represent ongoing spheres of activity with standards to maintain (e.g. Cycling, Habits, Health, NAS, Technology). Sentry checks that personal maintenance guides have not leaked into resource inboxes.
- **Resources (`05 - Knowledge` & `06 - Resources`)**: Distinguishes durable synthetic explanations and prompt libraries (`05 - Knowledge`) from external source captures, book notes, and video digests (`06 - Resources`).
- **Archive (`10 - Archive`)**: Evaluates whether completed projects, superseded indexes, and time-decaying contract research are actively moved to cold storage.

### Layer 2: Shared Space (`02 - Taani`) PARA Conformance
Shared household spaces typically organize by subject domain (`Finance/`, `Food/`, `House/`, `Travel/`). `vault-sentry` audits the implicit PARA health inside these shared domains:
- **Shared Projects**: Finite household DIY tasks, renovation projects, and trip itineraries.
- **Shared Areas**: Operational systems, recurring cleaning routines, cooking systems, and financial checkpoints.
- **Shared Resources**: Recipe collections (`Rxxx`), appliance manuals, homeware wishlists, and travel inspiration.
- **Shared Archives**: Historical conveyancing, old property listings, and expired broadband deals.
- **Structural Conflation Diagnosis**: Flags unpartitioned flat folders (e.g. `House/`) that conflate all four tiers into a single directory, proposing either thematic subfolder clusters (`Renovation/`, `Cleaning/`, `Appliances/`, `Property/`) or unified frontmatter metadata (`para: project | area | resource | archive`).

---

## 4. Iconize Expected Page Icon Audit

Obsidian Iconize configuration is audited via `.obsidian/plugins/obsidian-icon-folder/data.json`:
- **Folder Icons**: Verified for Lucide icons (`Li...`) matching the domain purpose (e.g. `02 - Taani/Food` $\rightarrow$ `LiUtensils`, `04 - Areas/Habits` $\rightarrow$ `LiFlame`, `11 - Agents/Audits` $\rightarrow$ `LiShieldCheck`).
- **Index Notes**: Verified for consistent Lucide icons matching their parent directory or domain concept.
- **Book Summaries**: Verified for literature emoji (`📚`).
- **Agent Notes**: Verified against the Vault Constitution and Note Standards requiring `🤖` for all notes under `11 - Agents/`.
- **Content Leaves**: Verified for topical emojis (e.g. `🍳` for recipes, `🚲` for cycling, `🏃` for running, `📊` for financial dashboards).

The audit outputs coverage percentages, an inventory of missing expected icons, and a staged JSON patch ready to merge safely into `data.json`.

---

## 5. Note Destination Routing Engine (`--suggest`)

When creating a new note or triaging an incoming draft, `vault-sentry` determines the canonical destination based on the Vault Constitution:

```bash
# Suggest destination from note title or concept
python3 scripts/vault-sentry.py --suggest "Air Fryer Sourdough Pizza Recipe"

# Suggest destination from a draft file
python3 scripts/vault-sentry.py --suggest-file /path/to/draft.md

# Machine-readable JSON output
python3 scripts/vault-sentry.py --suggest "Running my first Half Marathon" --json
```

### Routing Output Schema:
1. **Recommended Folder**: Canonical vault directory path.
2. **Recommended File Name**: Standardized, clean filename (e.g. `R012 - Sourdough Pizza.md` for recipes).
3. **Parent Index Note**: Wikilink to parent index for immediate integration into the navigation graph.
4. **Recommended Tags**: 2–4 lowercase taxonomy tags.
5. **Recommended Icon**: Lucide ID (`Li...`) or topical emoji.
6. **PARA Tier**: `Project (Shared/Personal)`, `Area (Shared/Personal)`, `Resource`, `Knowledge`, or `Archive`.
7. **Classification Rationale**: Exact constitutional rules explaining why it belongs here.
8. **Frontmatter Scaffold**: Copy-paste ready YAML header with `parent` and `tags`.
9. **Alternative Destination**: Second-best destination and explicit trade-off rationale.

---

## 6. Note Placement & Relocation ("Where It Should Live Instead")

Notes frequently suffer from domain drift or accidental dumping into generic folders. `vault-sentry` enforces the **Vault Constitution classification rules**:
- **Project**: Finite outcome with a completion condition or target date.
- **Area**: Ongoing perpetual responsibility or maintained domain.
- **Knowledge**: Durable explanation, permanent technical concept, prompt library, or curriculum.
- **Resource**: External saved source, book summary, YouTube summary, or third-party article.
- **Journal**: Time-based records, daily notes, quick logs.
- **Taani**: Shared household domains (Finance, House, Travel) with joint governance.
- **Archive**: Inactive, superseded, completed, or historical material.

### Relocation Heuristics:
1. **Misplaced Notes in Resource Inboxes**:
   - Notes covering running races or fitness in `06 - Resources/AI` $\rightarrow$ Relocate to `04 - Areas/Health and Fitness/`.
   - Notes covering bike repairs or cycling endurance in `06 - Resources/AI` $\rightarrow$ Relocate to `04 - Areas/Cycling/`.
   - Notes covering home water filters or coffee brewing in `06 - Resources/AI` $\rightarrow$ Relocate to `02 - Taani/House/`.
2. **De-cluttering Overloaded Flat Folders**:
   - Proposes thematic subfolder clusters for overloaded areas (e.g. `02 - Taani/House/` into `Cleaning/`, `Appliances/`, `Furnishing/`, `Renovation/`, `Property/`).

---

## 7. Staleness & Archival Heuristics ("Suggest Notes to Archive")

`vault-sentry` identifies candidates for moving to `10 - Archive/` using four signals:

1. **Dead & Superseded Indexes**:
   - Index notes whose contents have migrated to other canonical areas (e.g. `05 - Knowledge/Finance Index.md` after Finance migrated to `02 - Taani/Finance`).
2. **Time-Decaying & Expired Research**:
   - Time-sensitive buying guides and contract deals that lose accuracy over time (e.g. `Best Broadband Deal.md`, expired mortgage research).
3. **Completed Finite Projects & Past Trips**:
   - Trip plans, itineraries, and packing lists whose travel dates have passed (e.g. `Amsterdam 2026 - Packing List.md` pattern).
4. **Untouched Stale Leaves**:
   - Leaf notes with $\le 1$ inbound link and unmodified for $>40$ days that have been superseded by newer notes (e.g. `Bedding set.md` superseded by `Best Bedding and Linen sets.md`).

---

## 8. The 36 Diagnostic Dimensions

`vault-sentry` evaluates the vault across all 36 dimensions:
1. Safety Enforcement (Read-Only Default)
2. Architecture Understanding
3. Filesystem Health (Illegal chars, whitespace, zero-byte, case collisions)
4. Markdown Integrity (Heading jumps, unclosed fences, YAML syntax, Git conflict markers)
5. Wikilink & Link Integrity (WikiLinks, embeds, markdown links, anchor tags)
6. Orphan Notes (Isolated vs no-inbound)
7. Dead-End & Weakly Connected Notes
8. Duplicate & Near-Duplicate Content
9. Frontmatter & Schema Drift
10. Tag Taxonomy (Case variants, singletons, template leaks)
11. Icon Health (`data.json` cross-check, missing folder icons)
12. Attachment Health (Reference integrity, phantom deleted references)
13. Structured Data Integrity (`.base` files, TSV, JSON)
14. Canonical vs Generated Data Boundaries
15. Automation & Machine Path Portability
16. Obsidian Core & Community Plugin Configuration
17. Dataview Query Health (Silent omissions, empty tables)
18. Template Health (Placeholder leaks, schema drift)
19. Navigation & Discoverability
20. Naming Convention Health
21. Date & Periodic Note Health
22. Shared / Private Boundaries
23. Git Repository Health (Untracked moves, deleted paths)
24. Sync Health (iCloud POSIX symlink limitations)
25. Empty & Stale Areas
26. Data Loss Risks
27. Health Scoring (14 categories, 0–100)
28. Severity Classification (P0 to P4)
29. Confidence Scoring (HIGH, MEDIUM, LOW)
30. Vault Health Report Generation
31. Machine-Readable Findings JSON
32. Repair Manifest Staging
33. Audit Metrics Summary Table
34. Value-First Principle
35. Diagnostic Clarity Principle
36. Final Top 10 Ranked Actions

---

## 9. Running Vault Sentry

```bash
# Full Vault Audit (Output defaults to "11 - Agents" inside the vault)
python3 ~/.codex/skills/planning/vault-sentry/scripts/vault-sentry.py \
  --vault "/path/to/vault"

# Note Destination Suggestion from title or topic
python3 ~/.codex/skills/planning/vault-sentry/scripts/vault-sentry.py \
  --suggest "Air Fryer Sourdough Pizza Recipe"

# Note Destination Suggestion from draft file
python3 ~/.codex/skills/planning/vault-sentry/scripts/vault-sentry.py \
  --suggest-file "/path/to/draft.md"

# Output Destination Suggestion as JSON
python3 ~/.codex/skills/planning/vault-sentry/scripts/vault-sentry.py \
  --suggest "Replacing Bathroom Spotlights" --json
```
