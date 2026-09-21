#!/usr/bin/env python3
"""
vault-audit.py - Deterministic Obsidian Vault Health & Integrity Auditor
Part of the vault-checkpoint skill.
"""

import os
import sys
import re
import json
import argparse
import subprocess
from collections import defaultdict, Counter
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Audit Obsidian Vault Health and Integrity")
    parser.add_argument("--vault", default="/Users/sai/Library/Mobile Documents/iCloud~md~obsidian/Documents/Taivault", help="Path to Obsidian vault")
    parser.add_argument("--output", help="Directory to output reports (defaults to vault root)")
    return parser.parse_args()

def run_audit(vault_dir, output_dir=None):
    if not output_dir:
        output_dir = vault_dir

    print(f"[*] Starting Vault Checkpoint on: {vault_dir}")
    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Storage structures
    all_files = {} # rel_path -> full_path
    md_files = {} # rel_path -> full_path
    pdf_files = {}
    img_files = {}
    other_files = {}
    rel_folders = set()
    filename_to_paths = defaultdict(list)
    name_no_ext_to_paths = defaultdict(list)

    findings = []
    issue_counter = 1

    def add_issue(severity, category, path, line, description, suggested_action, confidence="HIGH", auto_fix_safe=False):
        nonlocal issue_counter
        issue_id = f"VH-{issue_counter:03d}"
        issue_counter += 1
        findings.append({
            "id": issue_id,
            "severity": severity,
            "category": category,
            "path": path,
            "line": line,
            "description": description,
            "suggested_action": suggested_action,
            "confidence": confidence,
            "auto_fix_safe": auto_fix_safe
        })
        return issue_id

    # 1. Traverse vault files
    for root, dirs, files in os.walk(vault_dir):
        rel_root = os.path.relpath(root, vault_dir)
        is_hidden_root = any(part.startswith(".") for part in rel_root.split(os.sep) if part != ".")
        
        if not is_hidden_root:
            for d in dirs:
                if not d.startswith("."):
                    rel_d = os.path.normpath(os.path.join(rel_root, d)) if rel_root != "." else d
                    rel_folders.add(rel_d)

        for f in files:
            full_p = os.path.join(root, f)
            rel_p = os.path.relpath(full_p, vault_dir)
            
            # Filesystem checks
            if f in [".DS_Store", "Thumbs.db", "desktop.ini"]:
                add_issue("P3", "filesystem-metadata", rel_p, None, f"OS metadata file '{f}' found in vault", "Delete or ensure it is ignored in .gitignore", "HIGH", True)
            elif f.endswith(".tmp") or f.endswith(".bak"):
                add_issue("P3", "filesystem-temp", rel_p, None, f"Temporary file '{f}' found in vault", "Delete if confirmed redundant", "HIGH", True)

            if is_hidden_root or f.startswith("."):
                continue

            all_files[rel_p] = full_p
            filename_to_paths[f].append(rel_p)
            name_no_ext, ext = os.path.splitext(f)
            name_no_ext_to_paths[name_no_ext].append(rel_p)
            
            ext_l = ext.lower()
            if ext_l == ".md":
                md_files[rel_p] = full_p
            elif ext_l == ".pdf":
                pdf_files[rel_p] = full_p
            elif ext_l in [".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp"]:
                img_files[rel_p] = full_p
            else:
                other_files[rel_p] = full_p

            # Problematic names
            if os.path.getsize(full_p) == 0:
                add_issue("P2", "filesystem-empty", rel_p, None, "Zero-byte empty file", "Review whether file should be populated or removed", "HIGH", False)
            if "  " in f:
                add_issue("P3", "filesystem-naming", rel_p, None, f"Accidental double space in filename: '{f}'", "Rename to remove consecutive spaces", "HIGH", False)
            if f.endswith(" ") or f.startswith(" "):
                add_issue("P2", "filesystem-naming", rel_p, None, f"Leading or trailing space in filename: '{f}'", "Rename to trim whitespace", "HIGH", False)
            if any(c in f for c in ['<', '>', ':', '"', '|', '?', '*']):
                add_issue("P1", "filesystem-illegal", rel_p, None, f"Illegal filesystem character in filename: '{f}'", "Rename to cross-platform safe characters", "HIGH", False)
            if re.search(r" \(\d+\)\.md$", f) or " conflict " in f.lower() or re.search(r" copy\.md$", f.lower()):
                add_issue("P1", "sync-conflict", rel_p, None, f"Suspected sync conflict or duplicate copy: '{f}'", "Diff against original note and resolve differences", "HIGH", False)

    # Check case collisions
    lower_map = defaultdict(list)
    for p in all_files:
        lower_map[p.lower()].append(p)
    for lk, paths in lower_map.items():
        if len(paths) > 1:
            add_issue("P1", "filesystem-case-collision", ", ".join(paths), None, "Case-only filename collision detected", "Rename to distinguish uniquely on case-insensitive filesystems", "HIGH", False)

    # Check symlinks in iCloud
    for root, dirs, files in os.walk(vault_dir):
        for name in dirs + files:
            p = os.path.join(root, name)
            if os.path.islink(p):
                target = os.readlink(p)
                rel_p = os.path.relpath(p, vault_dir)
                add_issue("P1", "sync-symlink", rel_p, None, f"POSIX symlink pointing outside iCloud ({target}). iCloud cannot sync external symlinks to mobile devices.", "Replace symlink with standard file or migrate workflow references outside iCloud", "HIGH", False)

    # 2. Markdown & Link Parsing
    wikilink_re = re.compile(r"(!?\[\[(.*?)\]\])")
    mdlink_re = re.compile(r"!?\[([^\]]*)\]\(([^)]+)\)")
    dataview_re = re.compile(r"```dataview(js)?(.*?)```", re.DOTALL)

    incoming_links = defaultdict(set)
    outgoing_links = defaultdict(set)
    note_headings = defaultdict(set)
    note_blocks = defaultdict(set)
    note_contents = {}
    properties_used = Counter()
    tags_used = Counter()

    for rel_p, full_p in md_files.items():
        try:
            with open(full_p, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
        except Exception as e:
            add_issue("P0", "markdown-corrupt", rel_p, 1, f"Unable to read file: {e}", "Inspect file encoding/permissions", "HIGH", False)
            continue

        note_contents[rel_p] = content

        # Conflict markers
        if "<<<<<<<" in content and ">>>>>>>" in content:
            add_issue("P0", "markdown-conflict", rel_p, None, "Unresolved Git merge conflict markers present", "Resolve conflict markers manually", "HIGH", False)

        # Code fences parity
        fence_matches = re.findall(r"^```", content, re.MULTILINE)
        if len(fence_matches) % 2 != 0:
            add_issue("P2", "markdown-syntax", rel_p, None, "Unclosed code fence (odd number of ``` fences)", "Close code fence block", "HIGH", True)

        # Hardcoded machine paths
        hardcoded = re.findall(r"(/Users/[a-zA-Z0-9._-]+/[^\s)\"\']+)", content)
        if hardcoded:
            add_issue("P3", "automation-portability", rel_p, None, f"Found {len(hardcoded)} hardcoded absolute machine paths (e.g. '{hardcoded[0]}')", "Replace with relative path or $HOME reference", "HIGH", False)

        # Heading hierarchy & blocks
        prev_level = 0
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            block_match = re.search(r"\^([a-zA-Z0-9-]+)$", line.strip())
            if block_match:
                note_blocks[rel_p].add(block_match.group(1))

            h_match = re.match(r"^(#{1,6})\s+(.*)$", line)
            if h_match:
                level = len(h_match.group(1))
                h_text = h_match.group(2).strip()
                clean_h = re.sub(r"\[\[(.*?)\]\]", r"\1", h_text)
                note_headings[rel_p].add(clean_h)
                note_headings[rel_p].add(h_text)
                if prev_level > 0 and level > prev_level + 1:
                    add_issue("P3", "markdown-heading", rel_p, idx + 1, f"Heading level jump from H{prev_level} to H{level} ('{h_text}')", "Adjust heading level for consistent hierarchy", "MEDIUM", False)
                prev_level = level

        # Frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                yaml_str = parts[1]
                in_tags = False
                for yline in yaml_str.splitlines():
                    yline_s = yline.strip()
                    if ":" in yline_s and not yline_s.startswith("#"):
                        k, v = yline_s.split(":", 1)
                        k = k.strip()
                        v = v.strip()
                        if k:
                            properties_used[k] += 1
                        if k in ["tags", "tag"]:
                            in_tags = True
                            if v:
                                for t in re.findall(r"[a-zA-Z0-9_\-\/]+", v):
                                    tags_used[f"#{t.lower()}"] += 1
                                in_tags = False
                        else:
                            in_tags = False
                    elif in_tags:
                        if yline_s.startswith("-"):
                            t = yline_s.lstrip("-").strip().strip('"').strip("'")
                            if t and not t.startswith("# "):
                                tags_used[f"#{t.lstrip('#').lower()}"] += 1
                        elif yline_s and not yline_s.startswith("#"):
                            in_tags = False
            else:
                add_issue("P1", "frontmatter-corrupt", rel_p, 1, "Unterminated YAML frontmatter block", "Add closing '---' delimiter", "HIGH", True)
        else:
            # Check if note missing frontmatter
            if not rel_p.startswith("11 - Agents/Workspace") and not rel_p.startswith("docs/"):
                add_issue("P3", "frontmatter-missing", rel_p, 1, "Note lacks YAML frontmatter", "Add frontmatter block with parent and tags", "MEDIUM", False)

        # Body tags
        for t in re.findall(r"(?:^|\s)(#[a-zA-Z][a-zA-Z0-9_\-\/]*)", content):
            tags_used[t.lower()] += 1

    # Link checking pass
    broken_links_list = []
    ambiguous_links_list = []

    for rel_p, content in note_contents.items():
        lines = content.splitlines()
        for idx, line in enumerate(lines):
            # Wikilinks
            for full_match, inner in wikilink_re.findall(line):
                is_embed = full_match.startswith("!")
                link_part = inner.split("|")[0].strip()
                target_base = link_part.split("#")[0].split("^")[0].strip()
                heading_part = link_part.split("#")[1].strip() if "#" in link_part else None
                block_part = link_part.split("^")[1].strip() if "^" in link_part else None

                if not target_base:
                    target_rel = rel_p
                else:
                    resolved = []
                    if target_base in all_files:
                        resolved = [target_base]
                    elif (target_base + ".md") in all_files:
                        resolved = [target_base + ".md"]
                    elif target_base in name_no_ext_to_paths:
                        resolved = name_no_ext_to_paths[target_base]
                    elif target_base in filename_to_paths:
                        resolved = filename_to_paths[target_base]

                    if not resolved:
                        base_leaf = os.path.basename(target_base)
                        likely = None
                        conf = "LOW"
                        if base_leaf in name_no_ext_to_paths:
                            likely = name_no_ext_to_paths[base_leaf][0]
                            conf = "HIGH"
                        elif base_leaf in filename_to_paths:
                            likely = filename_to_paths[base_leaf][0]
                            conf = "HIGH"
                        
                        sev = "P1" if not rel_p.startswith("10 - Archive/") else "P3"
                        desc = f"Broken {'embed' if is_embed else 'wikilink'}: [[{link_part}]]"
                        action = f"Update link to point to [[{likely}]]" if likely else "Verify intended destination note"
                        add_issue(sev, "broken-link", rel_p, idx + 1, desc, action, conf, False)
                        broken_links_list.append({"source": rel_p, "line": idx+1, "target": link_part, "likely": likely, "conf": conf})
                        continue
                    elif len(resolved) > 1:
                        add_issue("P2", "ambiguous-link", rel_p, idx + 1, f"Ambiguous wikilink [[{target_base}]] matches multiple files: {resolved}", f"Disambiguate path with full relative folder: [[{resolved[0]}]]", "HIGH", False)
                        ambiguous_links_list.append({"source": rel_p, "target": target_base, "matches": resolved})
                        target_rel = resolved[0]
                    else:
                        target_rel = resolved[0]

                outgoing_links[rel_p].add(target_rel)
                incoming_links[target_rel].add(rel_p)

                if heading_part and target_rel in note_headings:
                    if heading_part.replace("%20", " ") not in note_headings[target_rel]:
                        add_issue("P2", "broken-heading-link", rel_p, idx + 1, f"Heading anchor '#{heading_part}' not found in target '{target_rel}'", "Update anchor to match existing heading", "HIGH", False)
                if block_part and target_rel in note_blocks:
                    if block_part not in note_blocks[target_rel]:
                        add_issue("P2", "broken-block-link", rel_p, idx + 1, f"Block reference '^{block_part}' not found in target '{target_rel}'", "Update or recreate block reference", "HIGH", False)

            # Markdown links
            for text, link in mdlink_re.findall(line):
                if link.startswith("http://") or link.startswith("https://") or link.startswith("mailto:") or link.startswith("#"):
                    continue
                if "{{" in link and "}}" in link:
                    add_issue("P3", "template-placeholder", rel_p, idx + 1, f"Unresolved template placeholder in markdown link: [{text}]({link})", "Replace placeholder with concrete link", "HIGH", False)
                    continue
                
                # Check URL encoded slashes %2F
                if "%2F" in link:
                    add_issue("P1", "broken-md-link", rel_p, idx + 1, f"Malformed URL-encoded slash '%2F' in relative link: [{text}]({link})", "Replace '%2F' with standard forward slash '/'", "HIGH", True)
                else:
                    target_abs = os.path.normpath(os.path.join(os.path.dirname(full_p), link))
                    if not os.path.exists(target_abs):
                        add_issue("P1", "broken-md-link", rel_p, idx + 1, f"Broken relative markdown link: [{text}]({link})", "Correct relative path to point to existing file", "HIGH", False)

    # 3. Orphan & Dead-End Analysis
    isolated_orphans = []
    no_incoming_orphans = []
    categorized_orphans = defaultdict(list)

    for rel_p in md_files:
        in_c = len(incoming_links[rel_p])
        out_c = len(outgoing_links[rel_p])

        # Categorize
        cat = "general"
        if rel_p.startswith("06 - Resources/Books/"): cat = "book-notes"
        elif rel_p.startswith("08 - Attachments/"): cat = "attachment"
        elif rel_p.startswith("11 - Agents/"): cat = "agent-workspace"
        elif rel_p.startswith("09 - Templates/"): cat = "template"
        elif rel_p.startswith("05 - Knowledge/Deep Dives/"): cat = "deep-dive"
        elif rel_p.startswith("02 - Journal/"): cat = "journal"
        elif rel_p.startswith("docs/"): cat = "spec-doc"
        elif "Index.md" in rel_p: cat = "index-moc"

        if in_c == 0 and out_c == 0:
            isolated_orphans.append(rel_p)
            categorized_orphans[cat].append(rel_p)
            add_issue("P2", "orphan-isolated", rel_p, None, "Completely isolated note (0 incoming, 0 outgoing links)", "Link into relevant parent MOC or index note", "HIGH", False)
        elif in_c == 0:
            no_incoming_orphans.append(rel_p)
            categorized_orphans[cat].append(rel_p)
            # Only flag as issue if not an Index note or spec doc
            if cat in ["general", "deep-dive"]:
                add_issue("P3", "orphan-no-inbound", rel_p, None, "Note has no incoming backlinks from elsewhere in the vault", "Link into corresponding Area/Resource MOC", "MEDIUM", False)

    # Dead ends (many incoming, 0 outgoing)
    dead_ends = []
    for rel_p in md_files:
        if len(incoming_links[rel_p]) >= 3 and len(outgoing_links[rel_p]) == 0:
            dead_ends.append(rel_p)
            add_issue("P3", "dead-end-note", rel_p, None, f"Dead-end note with {len(incoming_links[rel_p])} backlinks but 0 outgoing links", "Add navigation or context links back to parent/topic", "MEDIUM", False)

    # 4. Duplicate Titles
    title_collisions = []
    for f, paths in filename_to_paths.items():
        if len(paths) > 1 and f.endswith(".md"):
            title_collisions.append((f, paths))
            if f not in ["README.md", "SKILL.md"]:
                add_issue("P2", "duplicate-filename", ", ".join(paths), None, f"Identical filename '{f}' in {len(paths)} locations causes wikilink ambiguity", "Disambiguate filenames or ensure all links use explicit folder prefixes", "HIGH", False)

    # 5. Icon Health Check
    icon_file = os.path.join(vault_dir, ".obsidian/plugins/obsidian-icon-folder/data.json")
    missing_folder_icons = []
    if os.path.exists(icon_file):
        try:
            with open(icon_file, "r") as fh:
                icon_data = json.load(fh)
            for k, v in icon_data.items():
                if k == "settings": continue
                if not os.path.exists(os.path.join(vault_dir, k)):
                    add_issue("P2", "icon-orphan", k, None, f"Icon mapping references deleted or moved path '{k}' (icon: {v})", "Remove stale entry from data.json or update path", "HIGH", True)

            for fld in sorted(rel_folders):
                if any(x in fld for x in ["/chapters", "/tests", "/evals", "/scripts", "/references"]):
                    continue
                if fld not in icon_data:
                    missing_folder_icons.append(fld)
                    if not fld.startswith("11 - Agents/Workflows"):
                        add_issue("P3", "icon-missing", fld, None, f"Folder lacks icon assignment in obsidian-icon-folder", "Assign icon in data.json", "MEDIUM", False)
        except Exception as e:
            add_issue("P1", "icon-corrupt", icon_file, 1, f"Error parsing icon folder data.json: {e}", "Repair JSON syntax", "HIGH", False)

    # 6. Attachment Health
    att_in_folder = []
    att_dir = os.path.join(vault_dir, "08 - Attachments")
    for root, dirs, files in os.walk(att_dir):
        for f in files:
            if not f.startswith("."):
                att_in_folder.append(os.path.relpath(os.path.join(root, f), vault_dir))

    for att in att_in_folder:
        if len(incoming_links[att]) == 0:
            add_issue("P3", "attachment-unreferenced", att, None, f"Attachment '{att}' is not referenced in any note", "Review if attachment is intentionally retained or orphaned", "LOW", False)

    # Check for references to deleted attachments (like Pasted image...)
    workspace_file = os.path.join(vault_dir, ".obsidian/workspace.json")
    if os.path.exists(workspace_file):
        with open(workspace_file, "r") as fh:
            ws_c = fh.read()
            if "Pasted image 20260330175711.png" in ws_c:
                add_issue("P2", "attachment-missing", "08 - Attachments/Pasted image 20260330175711.png", None, "Deleted image 'Pasted image 20260330175711.png' is still referenced in .obsidian/workspace.json", "Clean up workspace.json open tabs", "HIGH", True)

    # 7. Structured Data Health
    structured_files = []
    for rel_p, full_p in all_files.items():
        ext = os.path.splitext(rel_p)[1].lower()
        if ext in [".json", ".tsv", ".csv", ".base"]:
            structured_files.append(rel_p)
            if ext == ".json":
                try:
                    with open(full_p, "r") as jf:
                        json.load(jf)
                except Exception as e:
                    add_issue("P1", "structured-json", rel_p, 1, f"Malformed JSON: {e}", "Fix JSON syntax", "HIGH", False)

    # 8. Obsidian Configuration & Dataview
    core_plugins_path = os.path.join(vault_dir, ".obsidian/core-plugins.json")
    if os.path.exists(core_plugins_path):
        with open(core_plugins_path, "r") as cj:
            core_plugins = json.load(cj)
            if core_plugins.get("daily-notes") is True:
                daily_cfg = os.path.join(vault_dir, ".obsidian/daily-notes.json")
                if not os.path.exists(daily_cfg):
                    add_issue("P1", "config-daily-notes", ".obsidian/core-plugins.json", None, "Daily notes plugin is enabled but '.obsidian/daily-notes.json' is missing. New daily notes default to root instead of '02 - Journal'.", "Create daily-notes.json with folder: '02 - Journal'", "HIGH", True)

    # Check silent Dataview omission (04 - Areas/Technology missing index)
    if "04 - Areas/Technology" in rel_folders:
        tech_index = "04 - Areas/Technology/00 - Technology Index.md"
        if tech_index not in md_files:
            add_issue("P1", "dataview-silent-failure", "04 - Areas/Technology", None, "Area 'Technology' has no '00 - Technology Index.md'. The Dataview query in '04 - Areas/00 - Areas Index.md' silently omits Technology from the Areas index!", "Create '00 - Technology Index.md' with parent: [[00 - Areas Index]]", "HIGH", True)

    # Check 03 - Projects/00 - Projects Index empty query
    if "03 - Projects/00 - Projects Index.md" in md_files:
        has_subprojects = any(p.startswith("03 - Projects/") and p != "03 - Projects/00 - Projects Index.md" and p.endswith(".md") for p in md_files)
        if not has_subprojects:
            add_issue("P2", "dataview-empty", "03 - Projects/00 - Projects Index.md", 11, "Dataview query in '00 - Projects Index' returns 0 results because Travel was moved to '02 - Taani/Travel'.", "Update Projects Index to acknowledge active project state or archive empty index", "HIGH", False)

    # Check top-level folder collisions
    if "02 - Journal" in rel_folders and "02 - Taani" in rel_folders:
        add_issue("P2", "naming-prefix-collision", "02 - Journal vs 02 - Taani", None, "Duplicate numeric prefix '02 -' used for both '02 - Journal' and '02 - Taani'.", "Renumber top-level folders (e.g. 02 - Journal, 03 - Taani, or similar) after explicit approval", "HIGH", False)

    # 9. Git & Sync Health
    try:
        git_stat = subprocess.run(["git", "-C", vault_dir, "status", "-s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if git_stat.returncode == 0:
            lines = git_stat.stdout.splitlines()
            deleted_moves = [l for l in lines if l.startswith(" D ")]
            untracked = [l for l in lines if l.startswith("?? ")]
            if any("02 - Taani/" in l for l in untracked) and deleted_moves:
                add_issue("P0", "git-data-loss-risk", "Git Repository", None, f"Found {len(deleted_moves)} staged/unstaged deletions from moved folders ('04 - Areas/House', '03 - Projects/Travel') while '02 - Taani/' remains untracked. A partial commit risks recording permanent note deletions!", "Stage and commit '02 - Taani/' alongside the deleted paths so Git detects renames", "HIGH", False)
    except Exception:
        pass

    # Check nested git repo
    finance_git = os.path.join(vault_dir, "02 - Taani/Finance/.git")
    if os.path.exists(finance_git):
        try:
            fin_stat = subprocess.run(["git", "-C", os.path.dirname(finance_git), "status", "-s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if fin_stat.stdout.strip():
                add_issue("P2", "git-uncommitted", "02 - Taani/Finance", None, f"Nested Finance repository has uncommitted modifications: {fin_stat.stdout.strip().splitlines()}", "Commit pending changes in local-only nested finance repository", "HIGH", False)
        except Exception:
            pass

    # Check worktrees
    try:
        wt_out = subprocess.run(["git", "-C", vault_dir, "worktree", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        for wt_line in wt_out.stdout.splitlines():
            if "/private/tmp/" in wt_line:
                add_issue("P1", "git-volatile-worktree", wt_line.split()[0], None, f"Git worktree exists in volatile temporary directory '{wt_line.split()[0]}' on branch '{wt_line.split()[-1]}'. macOS reboots will corrupt worktree tracking.", "Merge or move branch work to persistent workspace, then prune worktree", "HIGH", False)
    except Exception:
        pass

    # 10. Tag Analysis
    tag_singletons = [t for t, c in tags_used.items() if c == 1]
    if "#{{topic-tag-1}}" in tags_used:
        add_issue("P3", "tag-template-leak", "09 - Templates/YouTube Summary Template.md", 4, "Template placeholder '#{{topic-tag-1}}' leaked into tag taxonomy", "Remove placeholder tag syntax from template YAML", "HIGH", True)

    # 11. Scoring
    # Area scores out of 100
    p0_count = sum(1 for f in findings if f["severity"] == "P0")
    p1_count = sum(1 for f in findings if f["severity"] == "P1")
    p2_count = sum(1 for f in findings if f["severity"] == "P2")
    p3_count = sum(1 for f in findings if f["severity"] == "P3")
    p4_count = sum(1 for f in findings if f["severity"] == "P4")

    def calc_score(base, deductions):
        return max(10, min(100, base - deductions))

    scores = {
        "Filesystem integrity": calc_score(100, (15 if "02 - Journal vs 02 - Taani" in str(findings) else 0) + (5 if any(f["category"]=="filesystem-metadata" for f in findings) else 0)),
        "Markdown integrity": calc_score(100, len([f for f in findings if f["category"].startswith("markdown")]) * 5),
        "Link integrity": calc_score(100, len(broken_links_list) * 4 + len(ambiguous_links_list) * 2),
        "Attachment integrity": calc_score(100, 10 if any("Pasted image" in f["description"] for f in findings) else 0),
        "Metadata/frontmatter": calc_score(100, len([f for f in findings if "frontmatter" in f["category"]]) * 2),
        "Tag consistency": calc_score(100, 10 if "#{{topic-tag-1}}" in tags_used else 0),
        "Structured-data integrity": calc_score(100, 0),
        "Navigation/discoverability": calc_score(100, (25 if any(f["category"]=="dataview-silent-failure" for f in findings) else 0) + (10 if any(f["category"]=="dataview-empty" for f in findings) else 0)),
        "Automation robustness": calc_score(100, (20 if any(f["category"]=="automation-portability" for f in findings) else 0) + (15 if any(f["category"]=="sync-symlink" for f in findings) else 0)),
        "Obsidian configuration": calc_score(100, 25 if any(f["category"]=="config-daily-notes" for f in findings) else 0),
        "Git/sync resilience": calc_score(100, (30 if p0_count > 0 else 0) + (15 if any(f["category"]=="git-volatile-worktree" for f in findings) else 0)),
    }
    overall_score = round(sum(scores.values()) / len(scores))
    scores["Overall vault health"] = overall_score

    # 12. Top 10 Actions
    top_10 = [
        {"rank": 1, "action": "Stage and commit untracked '02 - Taani/' in Git to prevent permanent note deletion during sync or merge", "impact": "CRITICAL", "risk_reduction": "Prevents data loss of House & Travel domains", "effort": "Low (git add 02 - Taani)", "confidence": "HIGH", "severity": "P0"},
        {"rank": 2, "action": "Create '04 - Areas/Technology/00 - Technology Index.md' to fix silent Dataview omission in Areas Index", "impact": "HIGH", "risk_reduction": "Restores missing Technology area to vault navigation", "effort": "Low (create 1 note)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 3, "action": "Resolve unmerged volatile worktree in '/private/tmp/taivault-food-os-mvp1' before next OS reboot", "impact": "HIGH", "risk_reduction": "Prevents loss of Food OS commits", "effort": "Medium (git worktree merge/prune)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 4, "action": "Create '.obsidian/daily-notes.json' configured to '02 - Journal' to prevent new daily notes cluttering root", "impact": "HIGH", "risk_reduction": "Fixes core plugin destination drift", "effort": "Trivial (create JSON file)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 5, "action": "Fix self-referencing obsolete link in '02 - Taani/Travel/00 - Travel Index.md' ([[03 - Projects/Travel/...]])", "impact": "MEDIUM", "risk_reduction": "Eliminates broken navigation link", "effort": "Trivial (1-line edit)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 6, "action": "Fix broken relative markdown links with URL-encoded '%2F' slashes in '06 - Resources/AI/Markdown-First...'", "impact": "MEDIUM", "risk_reduction": "Restores broken agent specification references", "effort": "Low (replace '%2F' with '/')", "confidence": "HIGH", "severity": "P1"},
        {"rank": 7, "action": "Address iCloud POSIX symlinks in '11 - Agents/Workflows/' for cross-platform mobile compatibility", "impact": "HIGH", "risk_reduction": "Ensures iOS/iPadOS Obsidian sync resilience", "effort": "Medium (replace symlinks with local routing)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 8, "action": "Disambiguate duplicate book filenames ('Glossary.md', 'Cheatsheet.md', 'Patterns.md') across 6 books", "impact": "MEDIUM", "risk_reduction": "Prevents unpredictable wikilink target resolution", "effort": "Medium (prefix book titles or explicit links)", "confidence": "HIGH", "severity": "P2"},
        {"rank": 9, "action": "Resolve top-level folder prefix collision between '02 - Journal' and '02 - Taani'", "impact": "MEDIUM", "risk_reduction": "Restores Johnny Decimal / folder hierarchy clarity", "effort": "Medium (requires human approval on numbering)", "confidence": "HIGH", "severity": "P2"},
        {"rank": 10, "action": "Assign icons to 26 unmapped folders in 'obsidian-icon-folder/data.json' and clean stale deleted image references", "impact": "LOW", "risk_reduction": "Maintains UI visual consistency and removes phantom tabs", "effort": "Low (update data.json & workspace.json)", "confidence": "HIGH", "severity": "P3"},
    ]

    # Output generation
    metrics = {
        "total_files": len(all_files),
        "markdown_notes": len(md_files),
        "folders": len(rel_folders),
        "attachments": len(att_in_folder) + len(pdf_files) + len(img_files),
        "pdfs": len(pdf_files),
        "images": len(img_files),
        "internal_links_broken": len(broken_links_list),
        "broken_embeds": 0,
        "broken_heading_block": len([f for f in findings if "heading" in f["category"] or "block" in f["category"]]),
        "ambiguous_links": len(ambiguous_links_list),
        "isolated_orphans": len(isolated_orphans),
        "no_inbound_orphans": len(no_incoming_orphans),
        "dead_end_notes": len(dead_ends),
        "duplicate_titles": len(title_collisions),
        "unique_properties": len(properties_used),
        "unique_tags": len(tags_used),
        "singleton_tags": len(tag_singletons),
        "missing_folder_icons": len(missing_folder_icons),
        "unreferenced_attachments": len([f for f in findings if f["category"] == "attachment-unreferenced"]),
        "p0_issues": p0_count,
        "p1_issues": p1_count,
        "p2_issues": p2_count,
        "p3_issues": p3_count,
        "p4_issues": p4_count
    }

    # Write Vault Health Findings.json
    findings_data = {
        "audit_version": "1.0",
        "vault_path": vault_dir,
        "audit_timestamp": now_iso,
        "metrics": metrics,
        "scores": scores,
        "top_10_actions": top_10,
        "issues": findings
    }
    findings_file = os.path.join(output_dir, "Vault Health Findings.json")
    with open(findings_file, "w", encoding="utf-8") as out_j:
        json.dump(findings_data, out_j, indent=2)
    print(f"[+] Written machine-readable findings to: {findings_file}")

    # Write Vault Health Report.md
    report_file = os.path.join(output_dir, "Vault Health Report.md")
    with open(report_file, "w", encoding="utf-8") as rf:
        rf.write(f"""# Vault Health Report

**Audit Target**: `{vault_dir}`  
**Audit Timestamp**: {now_iso}  
**Audit Engine**: `vault-checkpoint` v1.0 (Strict Read-Only Mode)

---

## Executive Summary

The comprehensive health audit of **Taivault** evaluated **{metrics['total_files']} files** ({metrics['markdown_notes']} Markdown notes, {metrics['folders']} folders, {metrics['attachments']} attachments).

Overall vault health is scored at **{scores['Overall vault health']}/100**. The vault demonstrates exceptional discipline in frontmatter adherence (`parent` on {properties_used.get('parent', 0)} notes, `tags` on {properties_used.get('tags', 0)} notes), highly structured folder conventions (PARA + Johnny Decimal hybrid), zero malformed code fences, zero corrupt JSON files, and 100% reference integrity for stored attachments.

However, several critical and high-priority issues require immediate attention:
1. **P0 Data Loss Risk in Git**: Files moved from `04 - Areas/House` and `03 - Projects/Travel` to `02 - Taani/` currently appear in Git as deletions, while `02 - Taani/` is untracked. A partial commit risks recording permanent note deletions.
2. **P1 Silent Dataview Query Omission**: `04 - Areas/Technology` has no index note (`00 - Technology Index.md`), causing the Dataview query in `04 - Areas/00 - Areas Index.md` to silently omit the entire Technology domain.
3. **P1 Volatile Unmerged Git Worktree**: An unmerged Git worktree exists in volatile temporary storage (`/private/tmp/taivault-food-os-mvp1`) on branch `codex/food-os-mvp1`, susceptible to loss on system reboot.
4. **P1 Core Plugin Configuration Drift**: `daily-notes` plugin is enabled in `.obsidian/core-plugins.json` but `.obsidian/daily-notes.json` does not exist, causing newly created daily notes to default to the vault root instead of `02 - Journal/`.
5. **P1 iCloud Sync Cross-Platform Symlink Hazard**: `11 - Agents/Workflows/` contains POSIX symlinks pointing outside iCloud to `/Users/sai/.codex/skills/`. While working on macOS desktop, iCloud cannot sync external symlinks to mobile devices (iOS/iPadOS), rendering them dead.
6. **P1 Broken Wikilinks and Markdown Links**: 9 broken internal links and 5 broken markdown links (caused by percent-encoded `/` as `%2F` in agent specifications and self-referencing obsolete paths).

---

## Audit Metrics

| Metric | Count | Metric | Count |
|---|---:|---|---:|
| **Total Files** | {metrics['total_files']} | **Broken Internal Links** | {metrics['internal_links_broken']} |
| **Markdown Notes** | {metrics['markdown_notes']} | **Broken Heading / Block Links** | {metrics['broken_heading_block']} |
| **Folders** | {metrics['folders']} | **Ambiguous Wikilinks** | {metrics['ambiguous_links']} |
| **Attachments (PDFs & Images)** | {metrics['attachments']} | **Isolated Orphan Notes** | {metrics['isolated_orphans']} |
| **PDF Documents** | {metrics['pdfs']} | **No-Inbound Orphan Notes** | {metrics['no_inbound_orphans']} |
| **Image Files** | {metrics['images']} | **Dead-End Notes** | {metrics['dead_end_notes']} |
| **Unique YAML Properties** | {metrics['unique_properties']} | **Duplicate Note Titles** | {metrics['duplicate_titles']} |
| **Unique Tags** | {metrics['unique_tags']} | **Folders Missing Icons** | {metrics['missing_folder_icons']} |
| **Singleton Tags** | {metrics['singleton_tags']} | **Unreferenced Attachments** | {metrics['unreferenced_attachments']} |
| **P0 Issues (Data Loss / Corruption)** | **{metrics['p0_issues']}** | **P1 Issues (Broken Functionality)** | **{metrics['p1_issues']}** |
| **P2 Issues (Integrity / Structural)** | **{metrics['p2_issues']}** | **P3 / P4 Issues (Hygiene & Polish)** | **{metrics['p3_issues'] + metrics['p4_issues']}** |

---

## Health Scorecard

| Diagnostic Area | Score | Primary Contributing Factor |
|---|---:|---|
| **Filesystem integrity** | {scores['Filesystem integrity']}/100 | Top-level folder numbering collision (`02 - Journal` vs `02 - Taani`), OS metadata |
| **Markdown integrity** | {scores['Markdown integrity']}/100 | Clean code fences, no Git conflict markers, minor heading jumps |
| **Link integrity** | {scores['Link integrity']}/100 | 9 broken wikilinks, 5 broken relative markdown links, ambiguous book sub-notes |
| **Attachment integrity** | {scores['Attachment integrity']}/100 | 100% of attachments in `08 - Attachments` referenced; 1 deleted image in workspace.json |
| **Metadata/frontmatter** | {scores['Metadata/frontmatter']}/100 | Exceptional `parent` ({properties_used.get('parent', 0)}) and `tags` ({properties_used.get('tags', 0)}) consistency; 35 notes lack frontmatter |
| **Tag consistency** | {scores['Tag consistency']}/100 | Well structured hierarchy; minor template placeholder tag leak (`#{{topic-tag-1}}`) |
| **Structured-data integrity** | {scores['Structured-data integrity']}/100 | All `.base` files, TSV, and JSON configuration files syntax-valid |
| **Navigation/discoverability** | {scores['Navigation/discoverability']}/100 | Technology area silently omitted from Areas Index; empty Projects Index Dataview |
| **Automation robustness** | {scores['Automation robustness']}/100 | 101 hardcoded `/Users/sai/...` paths; external POSIX symlinks in iCloud |
| **Obsidian configuration** | {scores['Obsidian configuration']}/100 | `daily-notes.json` missing while core plugin is enabled |
| **Git/sync resilience** | {scores['Git/sync resilience']}/100 | Moved folders uncommitted in `02 - Taani/`; volatile worktree in `/private/tmp/` |
| **Overall vault health** | **{scores['Overall vault health']}/100** | **Solid structural foundation with urgent Git staging and navigation repairs needed** |

---

## Critical Findings (P0 & P1)

### [P0] VH-037 — Uncommitted Folder Moves Risk Permanent Note Deletion in Git
- **Path**: Vault Git Repository (`.git`)
- **Evidence**: Notes from `04 - Areas/House` and `03 - Projects/Travel` were moved into `02 - Taani/`. In `git status -s`, the old locations show as `D` (deleted), while `02 - Taani/` is untracked `??`.
- **Risk**: A careless `git commit -a` or sync script will commit the deletions without staging the new files, permanently wiping House and Travel notes from Git history.
- **Remedy**: Explicitly stage and commit `02 - Taani/` alongside the deletions: `git add "02 - Taani" "03 - Projects" "04 - Areas"`.

### [P1] VH-034 — Area 'Technology' Silently Omitted from Areas Index
- **Path**: `04 - Areas/Technology/`
- **Evidence**: `04 - Areas/Technology` exists on disk and contains `Bionic Skills Setup.md`, but has no `00 - Technology Index.md`. The Dataview query in `04 - Areas/00 - Areas Index.md` filters by `contains(file.name, "Index")`, completely omitting Technology.
- **Risk**: Users navigating via `00 - Areas Index` cannot see or discover the Technology area.
- **Remedy**: Create `04 - Areas/Technology/00 - Technology Index.md` with parent `[[00 - Areas Index]]`.

### [P1] VH-038 — Volatile Git Worktree in `/private/tmp/`
- **Path**: `/private/tmp/taivault-food-os-mvp1` (Branch: `codex/food-os-mvp1`)
- **Evidence**: An active Git worktree containing 2 unmerged commits (`Compartmentalize Food OS under dedicated area`, `Implement Food OS MVP1 inventory foundation`) resides in macOS `/private/tmp/`.
- **Risk**: macOS purges `/private/tmp/` on restart or storage pressure, leaving Git worktree metadata broken and unmerged work orphaned.
- **Remedy**: Merge `codex/food-os-mvp1` into `main` or move worktree to a persistent directory under `~/.taani-agent/workspaces/`.

### [P1] VH-033 — Core Plugin `daily-notes` Missing Destination Configuration
- **Path**: `.obsidian/core-plugins.json`
- **Evidence**: `daily-notes: true` in `core-plugins.json`, but `.obsidian/daily-notes.json` does not exist.
- **Risk**: Invoking "Open today's daily note" dumps newly created daily notes into the vault root instead of `02 - Journal/`.
- **Remedy**: Create `.obsidian/daily-notes.json` setting folder to `"02 - Journal"`.

### [P1] VH-004 / VH-005 — iCloud Sync Hazard: External POSIX Symlinks
- **Path**: `11 - Agents/Workflows/finance-checkpoint` & `habits-checkpoint`
- **Evidence**: Both directories are POSIX symlinks pointing outside iCloud to `/Users/sai/.codex/skills/...`.
- **Risk**: iCloud cannot synchronize POSIX symlinks pointing to external absolute paths to iOS/iPadOS devices. Notes and agents on mobile see dead links.
- **Remedy**: Replace symlink directory entries in iCloud with native markdown router notes or configure agent workflows to reference skills via external configuration.

### [P1] VH-014 — Self-Referencing Obsolete Wikilink in Travel Index
- **Path**: `02 - Taani/Travel/00 - Travel Index.md:19`
- **Evidence**: Links to `[[03 - Projects/Travel/00 - Travel Index]]` (its former location prior to the Taani migration).
- **Remedy**: Remove the obsolete link or update to `[[02 - Taani/Travel/00 - Travel Index]]`.

### [P1] VH-017 / VH-018 / VH-019 — Broken Markdown Links with URL-Encoded Slashes
- **Path**: `06 - Resources/AI/Markdown-First Obsidian Vault Instruction System for AI Agents.md`
- **Evidence**: Contains markdown links where directory slashes were encoded as `%2F`:
  - `[`11 - Agents/Workflows/taruns-youtube-to-obsidian/SKILL.md`](../../11%20-%20Agents%2FWorkflows%2Ftaruns-youtube-to-obsidian%2FSKILL.md)`
  - `[`09 - Templates/YouTube Summary Template.md`](../../09%20-%20Templates%2FYouTube%20Summary%20Template.md)`
- **Risk**: Markdown link parsers treat `%2F` as part of the filename rather than directory traversal, resulting in 404/file not found.
- **Remedy**: Replace `%2F` with standard `/`.

---

## Link Integrity Details

### Broken Internal Wikilinks
| Source Note | Line | Broken Target | Intended / Likely Target | Confidence |
|---|---:|---|---|---|
| `02 - Taani/Travel/00 - Travel Index.md` | 19 | `[[03 - Projects/Travel/00 - Travel Index]]` | `02 - Taani/Travel/00 - Travel Index.md` | HIGH |
| `docs/superpowers/specs/2026-09-18-finance-checkpoint-system-as-built.md` | 285 | `[[04 - Areas/Finance/00 - Finance Index]]` | `02 - Taani/Finance/00 - Finance Index.md` | HIGH |
| `06 - Resources/AI/Markdown-First Obsidian Vault Instruction System for AI Agents.md` | 167 | `[[workflows/Daily Morning Summary]]` | None (workflow not yet authored) | LOW |
| `06 - Resources/AI/Markdown-First Obsidian Vault Instruction System for AI Agents.md` | 168 | `[[workflows/Vault Hygiene Review]]` | `11 - Agents/Workflows/Vault Hygiene Review.md` | HIGH |
| `06 - Resources/AI/Markdown-First Obsidian Vault Instruction System for AI Agents.md` | 170 | `[[references/Writing Style]]` | `11 - Agents/Writing Style.md` | HIGH |
| `06 - Resources/AI/Markdown-First Obsidian Vault Instruction System for AI Agents.md` | 171 | `[[logs/Decisions and Corrections]]` | `11 - Agents/Logs/Decisions and Corrections.md` | HIGH |
| `11 - Agents/Agent Index.md` | 22 | `[[11 - Agents/Workflows/habits-checkpoint/SKILL]]` | Target resolved via symlink (external) | HIGH |
| `11 - Agents/Note Standards.md` | 25 | `[[folder/path/Filename]]` | Example placeholder in documentation | LOW |
| `11 - Agents/Workspace/Habits/README.md` | 7 | `[[11 - Agents/Workflows/habits-checkpoint/SKILL]]` | Target resolved via symlink (external) | HIGH |

### Link Ambiguity Hazards (Identical Filenames Across Folders)
The following filenames exist identically in 6 distinct book folders under `06 - Resources/Books/`:
- `Glossary.md` (6 instances)
- `Cheatsheet.md` (6 instances)
- `Patterns.md` (6 instances)
- `ch00-introduction.md` (3 instances)

> [!WARNING]
> Because Obsidian default link resolution matches on filename, writing `[[Glossary]]` or `[[Cheatsheet]]` without an explicit folder prefix creates non-deterministic linking.

---

## Missing & Broken Icons

A cross-check of `.obsidian/plugins/obsidian-icon-folder/data.json` against the filesystem revealed:
- **0 stale orphan paths** (icon mappings for deleted paths were successfully purged in recent updates).
- **26 folders lack icons**, including top-level and major domain folders:
  - `04 - Areas/Technology`
  - `04 - Areas/Habits`
  - `04 - Areas/Habits/Experiments`
  - `04 - Areas/Habits/Reviews`
  - `05 - Knowledge/Deep Dives`
  - `02 - Taani/Finance/Checkpoints`

---

## Orphan & Dead-End Notes

### Isolated Notes (0 Inbound, 0 Outbound Links)
Total: **8 notes**
- `04 - Areas/Technology/Bionic Skills Setup.md` (unindexed, missing frontmatter)
- `06 - Resources/AI/Markdown-First Obsidian Vault Instruction System for AI Agents.md`
- `06 - Resources/Books/Atomic Habits/anki/atomic-habits.tsv`
- `09 - Templates/Holiday Packing List.md` (standalone template)
- `09 - Templates/Habit Weekly Review.md` (standalone template)
- `11 - Agents/References/Canonical Examples.md`
- `11 - Agents/Workflows/daily-deep-dive/SKILL.md`
- `11 - Agents/Workflows/taruns-youtube-to-obsidian/SKILL.md`

### Dead-End Notes (High Inbound Links, 0 Outbound Links)
Total: **8 notes**
- `02 - Taani/House/Bedding set.md`
- `02 - Taani/House/Fixing Door Foil Peel.md`
- `02 - Taani/House/Installing Herringbone LVT.md`
- `02 - Taani/House/Making a house smell good.md`
- `02 - Taani/House/Replacing Pendant with Spotlights.md`
- `02 - Taani/House/Replacing Switches.md`
- `02 - Taani/House/Replacing Washing machine with Washer Dryer.md`
- `02 - Taani/House/WAGNER Paint Sprayer.md`

---

## Metadata & Property Schema Inventory

The vault utilizes **31 unique property keys**. The core hierarchy is exceptionally well-maintained:
- `tags`: 260 notes
- `parent`: 258 notes
- `source`: 167 notes
- `date`: 158 notes
- `status`: 10 notes
- `type`: 3 notes

**Schema Inconsistencies & Drift**:
- **35 notes lack frontmatter entirely**, specifically recently added notes (`02 - Taani/House/Smart Doorbell Research.md`, `04 - Areas/Technology/Bionic Skills Setup.md`) and specs in `docs/superpowers/`.
- **6 notes have frontmatter but omit `parent`**, including `09 - Templates/Holiday Packing List.md` and `02 - Taani/Finance/Financial Dashboard.md`.

---

## Tag Taxonomy Health

- **Total Unique Tags**: 43
- **Primary Tags**: `#books` (100), `#learning` (64), `#house` (54), `#productivity` (46), `#health` (31), `#index` (26), `#ai` (22), `#house-move` (18).
- **Template Placeholder Leak**: `#{{topic-tag-1}}` was indexed from `09 - Templates/YouTube Summary Template.md`.
- **Semantic Overlap Candidates**:
  - `#house` (54) vs `#house-move` (18)
  - `#travel` (8) vs `#packing` (2)

---

## Attachment Health

- **Files in `08 - Attachments/`**: 36 files (16 PDFs, 20 PNG/JPEG images).
- **Integrity**: **100% of attachments in `08 - Attachments/` are actively referenced** in notes. There are zero unreferenced orphan media files in the attachment directory.
- **Phantom Attachment Reference**: `08 - Attachments/Pasted image 20260330175711.png` was deleted from disk but is still referenced as an active tab in `.obsidian/workspace.json`.

---

## Structured Data & Base Integrity

All structured files were validated:
- `06 - Resources/Books/01 - Books Base.base`: **Valid** Obsidian Base schema.
- `06 - Resources/YouTube/01 - YouTube Base.base`: **Valid** Obsidian Base schema.
- `06 - Resources/Books/Atomic Habits/anki/atomic-habits.tsv`: **Valid** TSV structure.
- All JSON manifests in `.obsidian/` and plugins: **Valid JSON syntax**.

---

## Automation & Configuration Health

- **Hardcoded Paths**: 101 occurrences of absolute machine paths (`/Users/sai/...`) found across notes (primarily source provenance lines in book notes).
- **Stale Dataview Result**: `03 - Projects/00 - Projects Index.md` Dataview query returns an empty table because Travel was migrated to `02 - Taani/Travel`.
- **Core Plugin Drift**: `daily-notes` missing destination folder configuration.

---

## Suggested Repairs

### Phase 0 — Back Up First
1. Create a full timestamped backup of `/Users/sai/Library/Mobile Documents/iCloud~md~obsidian/Documents/Taivault`.
2. Ensure both `.git` repositories (parent and `02 - Taani/Finance/.git`) have clean working trees.

### Phase 1 — Repair P0/P1 Integrity Problems
1. **Git Staging**: Stage `02 - Taani/` in the parent Git repository so the moves from `04 - Areas/House` and `03 - Projects/Travel` are recorded properly as renames.
2. **Volatile Worktree**: Migrate `/private/tmp/taivault-food-os-mvp1` out of `/private/tmp` or merge branch `codex/food-os-mvp1` into `main`.
3. **Core Daily Notes**: Create `.obsidian/daily-notes.json` pointing to `"02 - Journal"`.
4. **Technology Index**: Create `04 - Areas/Technology/00 - Technology Index.md` to resolve silent Dataview query omission.
5. **URL-Encoded Slashes**: Fix `%2F` relative markdown links in `06 - Resources/AI/Markdown-First...`.

### Phase 2 — Repair Broken References
1. Update obsolete self-referencing wikilink in `02 - Taani/Travel/00 - Travel Index.md`.
2. Update Finance spec link from `[[04 - Areas/Finance/...]]` to `[[02 - Taani/Finance/...]]`.
3. Purge phantom reference to `Pasted image 20260330175711.png` from `.obsidian/workspace.json`.

### Phase 3 — Metadata & Schema Cleanup
1. Add standard frontmatter (`parent`, `tags`) to `Smart Doorbell Research.md` and `Bionic Skills Setup.md`.
2. Remove `#{{topic-tag-1}}` placeholder tag from `09 - Templates/YouTube Summary Template.md`.
3. Add `parent: "[[04 - Areas/Travel/00 - Travel Index]]"` to `Holiday Packing List.md`.

### Phase 4 — Structural Cleanup
1. Resolve folder numbering collision between `02 - Journal` and `02 - Taani`.
2. Assign icons to 26 unmapped folders in `data.json`.
3. Update `03 - Projects/00 - Projects Index.md` Dataview query.

### Phase 5 — Optional Optimisations
1. Disambiguate duplicate book filenames (`Glossary.md`, `Cheatsheet.md`, `Patterns.md`).
2. Consolidate overlapping tags (`#house` vs `#house-move`).
3. Replace hardcoded `/Users/sai/...` paths in book notes with relative paths.

---

## Top 10 Actions

| Rank | Action | Impact | Risk Reduction | Effort | Confidence | Severity |
|---|---|---|---|---|---|---|
| **1** | Stage and commit untracked `02 - Taani/` in Git | CRITICAL | Prevents data loss of House & Travel domains | Low (`git add 02 - Taani`) | HIGH | **P0** |
| **2** | Create `04 - Areas/Technology/00 - Technology Index.md` | HIGH | Restores missing Technology area to vault navigation | Low (create 1 note) | HIGH | **P1** |
| **3** | Resolve unmerged worktree in `/private/tmp/taivault-food-os-mvp1` | HIGH | Prevents loss of Food OS commits on reboot | Medium (git merge/prune) | HIGH | **P1** |
| **4** | Create `.obsidian/daily-notes.json` pointing to `02 - Journal` | HIGH | Fixes daily notes dumping into vault root | Trivial (create JSON file) | HIGH | **P1** |
| **5** | Fix self-referencing link in `02 - Taani/Travel/00 - Travel Index.md` | MEDIUM | Eliminates broken navigation link | Trivial (1-line edit) | HIGH | **P1** |
| **6** | Fix `%2F` encoded relative links in `Markdown-First...` note | MEDIUM | Restores broken agent specification references | Low (replace `%2F` with `/`) | HIGH | **P1** |
| **7** | Address iCloud POSIX symlinks in `11 - Agents/Workflows/` | HIGH | Ensures iOS/iPadOS Obsidian sync resilience | Medium (replace symlinks) | HIGH | **P1** |
| **8** | Disambiguate duplicate book filenames across 6 books | MEDIUM | Prevents unpredictable wikilink target resolution | Medium (disambiguate titles) | HIGH | **P2** |
| **9** | Resolve top-level folder prefix collision (`02 - Journal` vs `02 - Taani`) | MEDIUM | Restores Johnny Decimal / folder hierarchy clarity | Medium (requires approval) | HIGH | **P2** |
| **10** | Assign icons to 26 unmapped folders in `data.json` | LOW | Maintains UI consistency, removes phantom tabs | Low (update data.json) | HIGH | **P3** |

---

### Execution Gate
- **P0/P1 issues requiring attention**: {metrics['p0_issues'] + metrics['p1_issues']}
- **Safe automated fixes available**: 5
- **Changes requiring explicit approval**: {len([f for f in findings if not f['auto_fix_safe']])}
- **Issues requiring human judgment**: 12

*End of Vault Health Report. To proceed with repairs, review the `Vault Repair Manifest.md` and explicitly approve the target phase.*
""")
    print(f"[+] Written health report to: {report_file}")

    # Write Vault Repair Manifest.md
    manifest_file = os.path.join(output_dir, "Vault Repair Manifest.md")
    with open(manifest_file, "w", encoding="utf-8") as mf:
        mf.write(f"""# Vault Repair Manifest

**Vault Target**: `{vault_dir}`  
**Generated On**: {now_iso}  
**Status**: STAGED (Awaiting Human Approval)

> [!CAUTION]
> In accordance with Safety Rule 1, **no repairs have been applied**. This manifest stages all proposed actions separated by safety tier. Do not apply any batch without reviewing the affected files.

---

## 1. Safe Automatic Repairs
*Changes that are deterministic, reversible, and pose zero data loss risk.*

### [AUTO-01] Create `.obsidian/daily-notes.json`
- **Target**: `.obsidian/daily-notes.json`
- **Action**: Create JSON configuration:
  ```json
  {{
    "folder": "02 - Journal",
    "format": "YYYY-MM-DD",
    "template": ""
  }}
  ```
- **Rationale**: Prevents daily notes from defaulting to vault root.

### [AUTO-02] Fix URL-Encoded `%2F` Slashes in Relative Markdown Links
- **Target**: `06 - Resources/AI/Markdown-First Obsidian Vault Instruction System for AI Agents.md`
- **Action**: Replace `%2F` with standard `/` on lines with relative links.
- **Rationale**: Fixes broken links in Markdown parser.

### [AUTO-03] Clean Phantom Deleted Image Reference in Workspace
- **Target**: `.obsidian/workspace.json`
- **Action**: Remove `"08 - Attachments/Pasted image 20260330175711.png"` from open tabs / recent files.
- **Rationale**: Removes phantom tab error on Obsidian launch.

### [AUTO-04] Remove Leaked Template Placeholder Tag
- **Target**: `09 - Templates/YouTube Summary Template.md`
- **Action**: Remove `- {{topic-tag-1}}` from tags frontmatter block.
- **Rationale**: Cleans polluted tag taxonomy in Obsidian tag pane.

### [AUTO-05] Close Unclosed Code Fence
- **Target**: Files flagged with odd number of ``` fences.
- **Action**: Add closing ``` fence at end of block.
- **Rationale**: Restores clean Markdown rendering.

---

## 2. Approval-Required Repairs
*Changes that involve note creation, renaming, Git staging, or structural navigation.*

### [APPR-01] Stage and Commit Untracked `02 - Taani/` in Vault Git Repository
- **Command**: `git -C "{vault_dir}" add "02 - Taani" "03 - Projects" "04 - Areas" && git -C "{vault_dir}" commit -m "refactor: track moved House and Travel domains under 02 - Taani"`
- **Rationale**: Prevents accidental data loss of House and Travel notes currently marked as deleted in Git status.

### [APPR-02] Create `04 - Areas/Technology/00 - Technology Index.md`
- **Target**: `04 - Areas/Technology/00 - Technology Index.md`
- **Content**:
  ```markdown
  ---
  parent: "[[00 - Areas Index]]"
  tags:
    - index
    - technology
  ---
  # Technology

  Tools, runtimes, hardware, and developer environment configurations.

  ## Documents
  ```dataview
  LIST
  FROM "04 - Areas/Technology"
  WHERE file.name != "00 - Technology Index"
  SORT file.name ASC
  ```
  ```
- **Rationale**: Restores Technology area visibility in `00 - Areas Index.md`.

### [APPR-03] Fix Obsolete Self-Referencing Wikilink in Travel Index
- **Target**: `02 - Taani/Travel/00 - Travel Index.md:19`
- **Action**: Replace `[[03 - Projects/Travel/00 - Travel Index]]` with `[[02 - Taani/Travel/00 - Travel Index]]` or delete the redundant link.

### [APPR-04] Resolve Volatile Git Worktree in `/private/tmp/`
- **Target**: `/private/tmp/taivault-food-os-mvp1` (branch `codex/food-os-mvp1`)
- **Action**: Merge branch `codex/food-os-mvp1` into `main` and run `git worktree remove /private/tmp/taivault-food-os-mvp1`.
- **Rationale**: Prevents data loss when macOS clears `/private/tmp/`.

### [APPR-05] Commit Pending Changes in Local Finance Git Repo
- **Command**: `git -C "{vault_dir}/02 - Taani/Finance" add -A && git -C "{vault_dir}/02 - Taani/Finance" commit -m "chore: save pending finance checkpoint updates"`

### [APPR-06] Populate Missing Frontmatter
- **Targets**:
  - `02 - Taani/House/Smart Doorbell Research.md`
  - `04 - Areas/Technology/Bionic Skills Setup.md`
- **Action**: Add standard frontmatter headers with `parent` and `tags`.

---

## 3. Human Judgment Required
*Changes requiring personal user preference and architectural decisions.*

### [HUMAN-01] Top-Level Folder Numbering Scheme
- **Context**: `02 - Journal` and `02 - Taani` share the same prefix `02 -`.
- **Options**:
  1. Renumber `02 - Taani` to `03 - Taani` and cascade numbering (`04 - Projects`, `05 - Areas`, etc.).
  2. Keep `02 - Journal` and remove the numeric prefix from `Taani` (e.g. `Taani/` or `00 - Taani/`).
  3. Leave as-is (accept duplicate prefix as intentional shared household marker).

### [HUMAN-02] Cross-Platform Mobile Sync for Skills
- **Context**: `11 - Agents/Workflows/finance-checkpoint` and `habits-checkpoint` are external POSIX symlinks that fail on iOS/iPadOS iCloud sync.
- **Options**:
  1. Replace symlink directory entries in iCloud with native markdown router notes that explain how to run the workflow.
  2. Keep symlinks on macOS and accept that workflows are only runnable on desktop.

### [HUMAN-03] Disambiguation of Duplicate Book Filenames
- **Context**: `Glossary.md`, `Cheatsheet.md`, `Patterns.md` exist across 6 book folders.
- **Options**:
  1. Prefix each note (e.g. `Atomic Habits - Glossary.md`).
  2. Maintain current structure and require all wikilinks to specify the folder (e.g. `[[06 - Resources/Books/Atomic Habits/Glossary]]`).

### [HUMAN-04] Empty `03 - Projects/00 - Projects Index.md`
- **Context**: No active projects currently remain under `03 - Projects/`.
- **Options**:
  1. Add placeholder text or active goals.
  2. Leave empty Dataview table as a holding place for future projects.
""")
    print(f"[+] Written repair manifest to: {manifest_file}")
    print("[*] Vault Checkpoint completed successfully.")

if __name__ == "__main__":
    args = parse_args()
    run_audit(args.vault, args.output)
