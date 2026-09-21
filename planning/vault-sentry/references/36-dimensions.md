# The 36 Diagnostic Dimensions of Vault Checkpoint

This reference details the 36 audit areas evaluated during an Obsidian vault checkpoint.

## 1. Safety & Boundaries
- **Safety Enforcement**: Default read-only operation. Zero mutations without explicit approval.
- **Architecture Understanding**: Mapping PARA, Johnny Decimal, inboxes, agent workspaces, canonical vs non-canonical areas.
- **Shared / Private Boundaries**: Verifying sensitive notes (Finance, ID docs, credentials) are quarantined and excluded from remote Git.

## 2. Filesystem & OS Layer
- **Invalid Characters**: Cross-platform path safety (`<`, `>`, `:`, `"`, `|`, `?`, `*`).
- **Whitespace Integrity**: Accidental double spaces, trailing or leading spaces in filenames.
- **Case Collisions**: Identical filenames differing only in capitalization on case-insensitive filesystems.
- **Suspicious Files**: Zero-byte files, `.tmp`, `.bak`, and sync collision copies (`(1)`, `copy`, `conflict`).
- **OS Metadata**: Lingering `.DS_Store`, `Thumbs.db`, or desktop files.

## 3. Markdown & Document Structure
- **Heading Hierarchy**: Enforcing sequential heading progression (no leaps from H1 to H3).
- **Code Fences**: Verifying matching, closed triple-backtick blocks.
- **Frontmatter Validity**: Valid YAML delimiters, syntax, and terminating markers.
- **Git Conflict Remnants**: Detecting leftover conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`).
- **Callout Syntax**: Standard Obsidian callout formatting (`> [!note]`).

## 4. Graph & Link Graph
- **Wikilink Resolution**: Resolving `[[Page]]`, `[[Page#Heading]]`, and `[[Page^block-id]]`.
- **Embed Resolution**: Validating transcluded notes and media `![[Target]]`.
- **Markdown Link Traversal**: Resolving relative paths `[Text](../path/file.md)`.
- **Ambiguous Link Hazards**: Detecting identical filenames in multiple subfolders that cause link collisions.
- **Confidence Scoring**: Grading suggested repairs as `HIGH`, `MEDIUM`, or `LOW`.

## 5. Network Connectivity & Topology
- **Isolated Orphans**: Notes with zero incoming and zero outgoing links.
- **No-Inbound Orphans**: Notes lacking inbound links from elsewhere in the vault.
- **Dead-End Notes**: Notes with multiple inbound links but zero outgoing links.
- **MOC & Index Integrity**: Ensuring Map of Content notes actively index existing children.

## 6. Duplication & Content Health
- **Title Collisions**: Identical filenames across directories.
- **Near-Duplicates**: Notes sharing high text similarity (differentiating template derivatives from divergent forks).

## 7. Metadata, Schemas & Tags
- **Property Schema Inventory**: Complete catalog of all YAML property keys and observed data types.
- **Schema Fragmentation**: Detecting redundant keys representing identical concepts (e.g. `date` vs `created`).
- **Tag Inventory & Singletons**: Listing all active tags and identifying single-use tags.
- **Tag Taxonomy Quality**: Detecting typo variants, singular/plural drift, and unparsed template tags (`#{{tag}}`).

## 8. Icons & Visual System
- **Plugin Cross-Check**: Reconciling `.obsidian/plugins/obsidian-icon-folder/data.json` against disk.
- **Orphan Icon Metadata**: Removing entries for files that were renamed or deleted.
- **Missing Folder Icons**: Flagging directories that lack assigned icons.

## 9. Attachments & Structured Assets
- **Attachment Inventory**: Auditing all files in `08 - Attachments/`.
- **Unreferenced Attachments**: Media retained on disk but never linked or embedded.
- **Referenced Missing Attachments**: Notes or workspace states referencing deleted media files.

## 10. Structured Data & Databases
- **Bases Files (`.base`)**: Validating YAML syntax and filter predicates.
- **Tabular Data (`.tsv`, `.csv`)**: Verifying table delimiters and column structure.
- **JSON Manifests**: Syntactic and structural validation of agent or plugin manifests.

## 11. Automation, Config & Synchronization
- **Portability**: Detecting hardcoded absolute machine paths (`/Users/username/...`).
- **Obsidian Core Config**: Reconciling enabled core plugins with required settings files (e.g. `daily-notes.json`).
- **Dataview Query Health**: Detecting queries that silently omit items due to missing index notes or folder moves.
- **Template Health**: Detecting unclosed template placeholders and outdated frontmatter schemas in `09 - Templates/`.
- **Git Repository Health**: Staging moved files, tracking unstaged changes, and verifying nested repos.
- **Volatile Worktrees**: Ensuring Git worktrees do not reside in volatile directories like `/private/tmp/`.
- **Sync & Mobile Resilience**: Flagging POSIX symlinks in iCloud that cannot synchronize to mobile devices.
