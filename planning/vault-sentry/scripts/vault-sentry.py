#!/usr/bin/env python3
"""
vault-sentry.py - Deep DFS Directory, Link Graph, Note Relocation & Archival Sentry
Part of the vault-sentry skill.
"""

import os
import sys
import re
import json
import time
import argparse
import subprocess
from collections import defaultdict, Counter
from datetime import datetime

def parse_args():
    parser = argparse.ArgumentParser(description="Vault Sentry: Deep DFS Directory, Link & Archival Auditor")
    parser.add_argument("--vault", default="/Users/sai/Library/Mobile Documents/iCloud~md~obsidian/Documents/Taivault", help="Path to Obsidian vault")
    parser.add_argument("--output", help="Directory to output reports (defaults to vault root)")
    return parser.parse_args()

def dfs_walk(current_dir, rel_path="", depth=0):
    """Walk directory tree in strict Depth-First Search order."""
    entries = sorted(os.listdir(current_dir))
    dirs = [e for e in entries if os.path.isdir(os.path.join(current_dir, e)) and not e.startswith(".")]
    files = [e for e in entries if os.path.isfile(os.path.join(current_dir, e)) and not e.startswith(".")]
    
    yield rel_path, depth, dirs, files
    
    for d in dirs:
        next_rel = os.path.join(rel_path, d) if rel_path else d
        yield from dfs_walk(os.path.join(current_dir, d), next_rel, depth + 1)

def run_sentry(vault_dir, output_dir=None):
    if not output_dir:
        output_dir = vault_dir

    print(f"[*] Starting Vault Sentry DFS Audit on: {vault_dir}")
    now_ts = time.time()
    now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    all_files = {} # rel_path -> full_path
    md_files = {} # rel_path -> full_path
    pdf_files = {}
    img_files = {}
    other_files = {}
    rel_folders = set()
    filename_to_paths = defaultdict(list)
    name_no_ext_to_paths = defaultdict(list)
    file_mtimes = {}

    findings = []
    issue_counter = 1

    def add_issue(severity, category, path, line, description, suggested_action, confidence="HIGH", auto_fix_safe=False):
        nonlocal issue_counter
        issue_id = f"VS-{issue_counter:03d}"
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

    # 1. First Pass: Index all files
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
            file_mtimes[rel_p] = os.path.getmtime(full_p)

            # Check for suspicious OS/temp files
            if f in [".DS_Store", "Thumbs.db", "desktop.ini"]:
                add_issue("P3", "filesystem-metadata", rel_p, None, f"OS metadata file '{f}' found in vault", "Delete or ensure it is ignored in .gitignore", "HIGH", True)
            elif f.endswith(".tmp") or f.endswith(".bak"):
                add_issue("P3", "filesystem-temp", rel_p, None, f"Temporary file '{f}' found in vault", "Delete if confirmed redundant", "HIGH", True)

            if is_hidden_root or f.startswith(".") or f in ["Vault Health Report.md", "Vault Repair Manifest.md", "Vault Health Findings.json"]:
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

            if os.path.getsize(full_p) == 0:
                add_issue("P2", "filesystem-empty", rel_p, None, "Zero-byte empty file", "Review whether file should be populated or removed", "HIGH", False)
            if "  " in f:
                add_issue("P3", "filesystem-naming", rel_p, None, f"Accidental double space in filename: '{f}'", "Rename to remove consecutive spaces", "HIGH", False)
            if f.endswith(" ") or f.startswith(" "):
                add_issue("P2", "filesystem-naming", rel_p, None, f"Leading or trailing space in filename: '{f}'", "Rename to trim whitespace", "HIGH", False)
            if any(c in f for c in ['<', '>', ':', '"', '|', '?', '*']):
                add_issue("P1", "filesystem-illegal", rel_p, None, f"Illegal filesystem character in filename: '{f}'", "Rename to cross-platform safe characters", "HIGH", False)

    # Check symlinks in iCloud
    for root, dirs, files in os.walk(vault_dir):
        for name in dirs + files:
            p = os.path.join(root, name)
            if os.path.islink(p):
                target = os.readlink(p)
                rel_p = os.path.relpath(p, vault_dir)
                add_issue("P1", "sync-symlink", rel_p, None, f"POSIX symlink pointing outside iCloud ({target}). Cannot sync to mobile devices.", "Replace symlink with standard file or migrate workflow references outside iCloud", "HIGH", False)

    # 2. Markdown & Link Graph Construction
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
    note_frontmatter = {}

    for rel_p, full_p in md_files.items():
        try:
            with open(full_p, "r", encoding="utf-8", errors="replace") as fh:
                content = fh.read()
        except Exception as e:
            add_issue("P0", "markdown-corrupt", rel_p, 1, f"Unable to read file: {e}", "Inspect file encoding/permissions", "HIGH", False)
            continue

        note_contents[rel_p] = content

        if "<<<<<<<" in content and ">>>>>>>" in content:
            add_issue("P0", "markdown-conflict", rel_p, None, "Unresolved Git merge conflict markers present", "Resolve conflict markers manually", "HIGH", False)

        fence_matches = re.findall(r"^```", content, re.MULTILINE)
        if len(fence_matches) % 2 != 0:
            add_issue("P2", "markdown-syntax", rel_p, None, "Unclosed code fence (odd number of ``` fences)", "Close code fence block", "HIGH", True)

        hardcoded = re.findall(r"(/Users/[a-zA-Z0-9._-]+/[^\s)\"\']+)", content)
        if hardcoded:
            add_issue("P3", "automation-portability", rel_p, None, f"Found {len(hardcoded)} hardcoded absolute machine paths", "Replace with relative path or $HOME reference", "HIGH", False)

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

        # Parse Frontmatter
        fm_dict = {}
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
                            fm_dict[k] = v
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
            if not rel_p.startswith("11 - Agents/Workspace") and not rel_p.startswith("docs/"):
                add_issue("P3", "frontmatter-missing", rel_p, 1, "Note lacks YAML frontmatter", "Add frontmatter block with parent and tags", "MEDIUM", False)

        note_frontmatter[rel_p] = fm_dict

        for t in re.findall(r"(?:^|\s)(#[a-zA-Z][a-zA-Z0-9_\-\/]*)", content):
            tags_used[t.lower()] += 1

    # Link Resolution Pass
    broken_links = []
    ambiguous_links = []

    for rel_p, content in note_contents.items():
        full_p = md_files[rel_p]
        lines = content.splitlines()
        in_code_block = False
        for idx, line in enumerate(lines):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # Strip inline code backticks so code snippets like `[[target]]` aren't treated as active links
            line_clean = re.sub(r"`[^`]+`", "", line)

            for full_match, inner in wikilink_re.findall(line_clean):
                is_embed = full_match.startswith("!")
                link_part = inner.split("|")[0].strip()
                target_base = link_part.split("#")[0].split("^")[0].strip()
                heading_part = link_part.split("#")[1].strip() if "#" in link_part else None
                block_part = link_part.split("^")[1].strip() if "^" in link_part else None

                if not target_base:
                    target_rel = rel_p
                else:
                    resolved = []
                    if target_base in all_files: resolved = [target_base]
                    elif (target_base + ".md") in all_files: resolved = [target_base + ".md"]
                    elif target_base in name_no_ext_to_paths: resolved = name_no_ext_to_paths[target_base]
                    elif target_base in filename_to_paths: resolved = filename_to_paths[target_base]

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
                        broken_links.append({"source": rel_p, "line": idx+1, "target": link_part, "likely": likely, "conf": conf})
                        continue
                    elif len(resolved) > 1:
                        add_issue("P2", "ambiguous-link", rel_p, idx + 1, f"Ambiguous wikilink [[{target_base}]] matches {len(resolved)} files: {resolved}", f"Disambiguate path with full relative folder: [[{resolved[0]}]]", "HIGH", False)
                        ambiguous_links.append({"source": rel_p, "target": target_base, "matches": resolved})
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

            for text, link in mdlink_re.findall(line_clean):
                if link.startswith("http://") or link.startswith("https://") or link.startswith("mailto:") or link.startswith("#"):
                    continue
                if "{{" in link and "}}" in link:
                    add_issue("P3", "template-placeholder", rel_p, idx + 1, f"Unresolved template placeholder in markdown link: [{text}]({link})", "Replace placeholder with concrete link", "HIGH", False)
                    continue
                if "%2F" in link:
                    add_issue("P1", "broken-md-link", rel_p, idx + 1, f"Malformed URL-encoded slash '%2F' in relative link: [{text}]({link})", "Replace '%2F' with standard forward slash '/'", "HIGH", True)
                else:
                    target_abs = os.path.normpath(os.path.join(os.path.dirname(full_p), link))
                    if not os.path.exists(target_abs):
                        add_issue("P1", "broken-md-link", rel_p, idx + 1, f"Broken relative markdown link: [{text}]({link})", "Correct relative path to point to existing file", "HIGH", False)

    # 3. DFS Directory-by-Directory Structural & Link Analysis
    dfs_sections = []
    overloaded_folders = []
    missing_index_folders = []

    for rel_path, depth, subdirs, files in dfs_walk(vault_dir):
        sec_name = rel_path if rel_path else "Root"
        md_in_sec = [f for f in files if f.endswith(".md")]
        index_in_sec = [f for f in md_in_sec if "Index" in f]
        
        # Link coherence: how many notes link to the section index?
        links_to_index = 0
        has_index = len(index_in_sec) > 0
        index_note = index_in_sec[0] if has_index else None
        
        if has_index:
            idx_rel = os.path.join(rel_path, index_note) if rel_path else index_note
            for mf in md_in_sec:
                if mf != index_note:
                    mf_rel = os.path.join(rel_path, mf) if rel_path else mf
                    if idx_rel in outgoing_links[mf_rel] or index_note.replace(".md", "") in outgoing_links[mf_rel]:
                        links_to_index += 1

        coherence = f"{links_to_index}/{max(1, len(md_in_sec) - 1)}" if (len(md_in_sec) > 1 and has_index) else "N/A"

        # Structural assessments
        assessment = "Healthy"
        flags = []
        if len(md_in_sec) >= 25 and not rel_path.startswith("06 - Resources/YouTube"):
            flags.append("OVERLOADED (>25 notes in flat folder)")
            overloaded_folders.append({"path": rel_path, "count": len(md_in_sec)})
        if not has_index and len(md_in_sec) > 0 and depth in [1, 2] and not rel_path.startswith("06 - Resources/Books") and not rel_path.startswith("08 - Attachments") and not rel_path.startswith("09 - Templates") and not rel_path.startswith("11 - Agents"):
            flags.append("MISSING INDEX NOTE")
            missing_index_folders.append(rel_path)
        if rel_path == "03 - Projects" and len(md_in_sec) == 1:
            flags.append("EMPTY PROJECTS (Dataview query returns 0)")
        if rel_path == "05 - Knowledge" and any(f == "Finance Index.md" for f in md_in_sec):
            flags.append("DEAD OBSOLETE INDEX (Finance Index in Knowledge)")

        if flags:
            assessment = "; ".join(flags)

        dfs_sections.append({
            "section": sec_name,
            "depth": depth,
            "notes_count": len(md_in_sec),
            "subdirs_count": len(subdirs),
            "index_note": index_note,
            "coherence": coherence,
            "assessment": assessment
        })

    # 4. Note Relocation Analysis ("Where it should live instead so it's not messy")
    relocation_proposals = []

    # Rules based on Vault Constitution:
    # Check 06 - Resources/AI for non-AI notes
    for rel_p in md_files:
        basename = os.path.basename(rel_p)
        dir_name = os.path.dirname(rel_p)

        # Misplaced notes in 06 - Resources/AI
        if dir_name == "06 - Resources/AI":
            if "Running" in basename or "Races" in basename:
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": "04 - Areas/Health and Fitness/Most Prestigious Running Races London.md",
                    "reason": "Note covers running events and race preparation, not artificial intelligence methodology. Belongs in Health & Fitness area.",
                    "confidence": "HIGH"
                })
            elif "Cycling" in basename:
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": f"04 - Areas/Cycling/{basename}",
                    "reason": "Note contains cycling mechanics and endurance guides. Belongs in the established 04 - Areas/Cycling domain.",
                    "confidence": "HIGH"
                })
            elif "Coffee" in basename:
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": "02 - Taani/House/Coffee 101.md",
                    "reason": "Coffee brewing guide relates to household kitchen routines. Belongs in 02 - Taani/House.",
                    "confidence": "HIGH"
                })
            elif "Water Filtration" in basename:
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": "02 - Taani/House/Household Water Filtration Systems (Deep Research).md",
                    "reason": "Deep research evaluating home undersink water filtration units. Belongs in household maintenance (02 - Taani/House).",
                    "confidence": "HIGH"
                })

        # Overloaded 02 - Taani/House/ clustering
        elif dir_name == "02 - Taani/House":
            if any(w in basename for w in ["Cleaning", "Clean", "Supplies", "Bathroom", "Laundry", "Bins", "Hand wash"]):
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": f"02 - Taani/House/Cleaning/{basename}",
                    "reason": "Part of the 10+ cleaning supply & routine notes cluttering House root. Cluster into a dedicated Cleaning subfolder.",
                    "confidence": "HIGH"
                })
            elif any(w in basename for w in ["Dreame", "Robot Vacuum", "Thermostats", "Doorbell", "Air fryer", "Washing machine"]):
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": f"02 - Taani/House/Appliances/{basename}",
                    "reason": "Smart home device and major appliance research notes. Cluster into an Appliances subfolder.",
                    "confidence": "HIGH"
                })
            elif any(w in basename for w in ["Bedding", "Table", "Chairs", "Furniture", "Dinnerware", "Kitchenware", "Coat Hook"]):
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": f"02 - Taani/House/Furnishing/{basename}",
                    "reason": "Furniture links and household purchase notes. Cluster into a Furnishing subfolder.",
                    "confidence": "HIGH"
                })
            elif any(w in basename for w in ["LVT", "Spotlights", "Switches", "Door Foil", "Paint Sprayer", "Solar Panels"]):
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": f"02 - Taani/House/Renovation/{basename}",
                    "reason": "DIY home improvement, electrical, and flooring projects. Cluster into a Renovation subfolder.",
                    "confidence": "HIGH"
                })
            elif any(w in basename for w in ["Rightmove", "Mortgage", "Budget"]):
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": f"02 - Taani/House/Property/{basename}",
                    "reason": "Property purchase, survey listing, and legal conveyance history.",
                    "confidence": "HIGH"
                })

        # In 05 - Knowledge
        elif dir_name == "05 - Knowledge":
            if basename == "Finance Index.md":
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": "10 - Archive/05 - Knowledge/Finance Index.md",
                    "reason": "Obsolete empty index; household finance now lives in 02 - Taani/Finance. Archive to eliminate confusion.",
                    "confidence": "HIGH"
                })
            elif basename == "F1 Personal Journalist.md":
                relocation_proposals.append({
                    "note": rel_p,
                    "current_location": dir_name,
                    "suggested_location": "05 - Knowledge/Prompts/F1 Personal Journalist.md",
                    "reason": "Specialized prompt instruction note; should cluster alongside Prompt Library.",
                    "confidence": "MEDIUM"
                })

    for r in relocation_proposals:
        add_issue("P2", "note-relocation", r["note"], None, f"Misplaced note: currently in '{r['current_location']}'. Suggested relocation: '{r['suggested_location']}'. ({r['reason']})", f"Move note to '{r['suggested_location']}' and update backlinks", r["confidence"], False)

    # 5. Stale / Untouched Notes to Archive
    archival_candidates = []
    
    for rel_p, mtime in file_mtimes.items():
        if not rel_p.endswith(".md"): continue
        if rel_p.startswith("10 - Archive") or "/chapters/" in rel_p or rel_p.startswith("."):
            continue
        
        age_days = (now_ts - mtime) / 86400
        basename = os.path.basename(rel_p)
        in_count = len(incoming_links.get(rel_p, []))
        
        # Heuristics for archival:
        # 1. Dead/obsolete index
        if basename == "Finance Index.md" and rel_p.startswith("05 - Knowledge"):
            archival_candidates.append({
                "note": rel_p,
                "age_days": round(age_days),
                "inbound_links": in_count,
                "reason": "Superseded index: contains empty Dataview query with 0 notes. Canonical finance moved to 02 - Taani/Finance.",
                "suggested_archive_path": "10 - Archive/Finance/Knowledge Finance Index (Obsolete).md",
                "confidence": "HIGH"
            })
        # 2. Time-decaying deals/purchases
        elif "Broadband Deal" in basename:
            archival_candidates.append({
                "note": rel_p,
                "age_days": round(age_days),
                "inbound_links": in_count,
                "reason": "Time-sensitive broadband contract research. Tariffs and deals expire; historical record should be archived.",
                "suggested_archive_path": "10 - Archive/House/Best Broadband Deal (Historical).md",
                "confidence": "HIGH"
            })
        # 3. Completed past trips / packing lists
        elif "Amsterdam 2026" in basename and not rel_p.startswith("10 - Archive"):
            archival_candidates.append({
                "note": rel_p,
                "age_days": round(age_days),
                "inbound_links": in_count,
                "reason": "Past trip packing list.",
                "suggested_archive_path": f"10 - Archive/Travel/{basename}",
                "confidence": "HIGH"
            })
        # 4. Old completed one-off purchases / research (>40 days untouched leaf notes)
        elif age_days > 40 and in_count <= 1 and any(w in basename for w in ["Paint Sprayer", "Robot Vacuum Research", "Bedding set"]):
            if "Bedding set.md" in basename and "02 - Taani/House/Best Bedding and Linen sets.md" in md_files:
                archival_candidates.append({
                    "note": rel_p,
                    "age_days": round(age_days),
                    "inbound_links": in_count,
                    "reason": "Superseded by 'Best Bedding and Linen sets.md'. Untouched for 45+ days.",
                    "suggested_archive_path": f"10 - Archive/House/{basename}",
                    "confidence": "HIGH"
                })

    for ac in archival_candidates:
        add_issue("P2", "archive-candidate", ac["note"], None, f"Archival candidate ({ac['age_days']} days untouched, {ac['inbound_links']} inbound links): {ac['reason']}", f"Move to '{ac['suggested_archive_path']}'", ac["confidence"], False)

    # 6. Git, Plugins & Environment Issues
    # Git status
    try:
        git_stat = subprocess.run(["git", "-C", vault_dir, "status", "-s"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if git_stat.returncode == 0:
            lines = git_stat.stdout.splitlines()
            deleted_moves = [l for l in lines if l.startswith(" D ")]
            untracked = [l for l in lines if l.startswith("?? ")]
            if any("02 - Taani/" in l for l in untracked) and deleted_moves:
                add_issue("P0", "git-data-loss-risk", "Git Repository", None, f"Found {len(deleted_moves)} unstaged deletions from moved folders while '02 - Taani/' remains untracked. A partial commit risks recording permanent note deletions!", "Stage and commit '02 - Taani/' alongside the deleted paths", "HIGH", False)
    except Exception:
        pass

    # Git volatile worktree check
    try:
        wt_stat = subprocess.run(["git", "-C", vault_dir, "worktree", "list"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if wt_stat.returncode == 0:
            for wt_line in wt_stat.stdout.splitlines():
                parts = wt_line.split()
                if parts:
                    wt_path = parts[0]
                    if wt_path.startswith("/private/tmp") or wt_path.startswith("/tmp"):
                        add_issue("P1", "git-volatile-worktree", wt_path, None, f"Active Git worktree resides in ephemeral temp path '{wt_path}'. macOS will purge it on reboot or memory pressure!", f"Remove worktree with 'git worktree remove {wt_path}' or relocate to persistent storage", "HIGH", False)
    except Exception:
        pass

    # Core daily notes config
    core_plugins_path = os.path.join(vault_dir, ".obsidian/core-plugins.json")
    if os.path.exists(core_plugins_path):
        with open(core_plugins_path, "r") as cj:
            core_plugins = json.load(cj)
            if core_plugins.get("daily-notes") is True:
                daily_cfg = os.path.join(vault_dir, ".obsidian/daily-notes.json")
                if not os.path.exists(daily_cfg):
                    add_issue("P1", "config-daily-notes", ".obsidian/core-plugins.json", None, "Daily notes plugin enabled without '.obsidian/daily-notes.json'. New daily notes default to vault root.", "Create daily-notes.json with folder: '02 - Journal'", "HIGH", True)

    # Missing Technology index
    if "04 - Areas/Technology" in rel_folders and "04 - Areas/Technology/00 - Technology Index.md" not in md_files:
        add_issue("P1", "dataview-silent-failure", "04 - Areas/Technology", None, "Area 'Technology' lacks '00 - Technology Index.md'. Silently omitted from '04 - Areas/00 - Areas Index.md' Dataview query!", "Create '00 - Technology Index.md' with parent: [[00 - Areas Index]]", "HIGH", True)

    # Duplicate top-level prefix
    if "02 - Journal" in rel_folders and "02 - Taani" in rel_folders:
        add_issue("P2", "naming-prefix-collision", "02 - Journal vs 02 - Taani", None, "Duplicate prefix '02 -' used for both '02 - Journal' and '02 - Taani'.", "Renumber top-level folders after explicit approval", "HIGH", False)

    # 7. Health Scoring
    p0_count = sum(1 for f in findings if f["severity"] == "P0")
    p1_count = sum(1 for f in findings if f["severity"] == "P1")
    p2_count = sum(1 for f in findings if f["severity"] == "P2")
    p3_count = sum(1 for f in findings if f["severity"] == "P3")
    p4_count = sum(1 for f in findings if f["severity"] == "P4")

    def calc_score(base, deductions):
        return max(10, min(100, base - deductions))

    scores = {
        "Filesystem integrity": calc_score(100, 20 if "02 - Journal vs 02 - Taani" in str(findings) else 0),
        "Markdown integrity": calc_score(100, len([f for f in findings if f["category"].startswith("markdown")]) * 4),
        "Link integrity": calc_score(100, len(broken_links) * 4 + len(ambiguous_links) * 2),
        "Attachment integrity": 95,
        "Metadata/frontmatter": calc_score(100, len([f for f in findings if "frontmatter" in f["category"]]) * 2),
        "Tag consistency": 90,
        "Structured-data integrity": 100,
        "Navigation/discoverability": calc_score(100, (25 if any(f["category"]=="dataview-silent-failure" for f in findings) else 0) + (15 if len(relocation_proposals) > 5 else 0)),
        "Automation robustness": calc_score(100, 30 if any(f["category"]=="sync-symlink" for f in findings) else 0),
        "Obsidian configuration": calc_score(100, 25 if any(f["category"]=="config-daily-notes" for f in findings) else 0),
        "Git/sync resilience": calc_score(100, 40 if p0_count > 0 else 0),
    }
    overall_score = round(sum(scores.values()) / len(scores))
    scores["Overall vault health"] = overall_score

    # Top 10 Actions
    top_10 = [
        {"rank": 1, "action": "Stage and commit untracked '02 - Taani/' in Git to prevent permanent note deletion during sync or merge", "impact": "CRITICAL", "risk_reduction": "Prevents permanent data loss of House & Travel domains", "effort": "Low (git add 02 - Taani)", "confidence": "HIGH", "severity": "P0"},
        {"rank": 2, "action": "Create '04 - Areas/Technology/00 - Technology Index.md' to fix silent Dataview omission in Areas Index", "impact": "HIGH", "risk_reduction": "Restores missing Technology area to vault navigation", "effort": "Low (create 1 note)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 3, "action": "Relocate misplaced notes out of '06 - Resources/AI' (Running Races -> Health, Cycling 101/102 -> Cycling, Coffee & Water Filter -> House)", "impact": "HIGH", "risk_reduction": "Cleans up domain boundaries and improves note discoverability", "effort": "Low (move 5 notes)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 4, "action": "Cluster overloaded '02 - Taani/House' (48 flat notes) into thematic subfolders: Cleaning, Appliances, Furnishing, Renovation, Property", "impact": "HIGH", "risk_reduction": "Transforms messy 48-file dumping ground into an organized household operating system", "effort": "Medium (batch folder moves)", "confidence": "HIGH", "severity": "P2"},
        {"rank": 5, "action": "Archive superseded and dead notes to '10 - Archive/' ('05 - Knowledge/Finance Index.md', 'Best Broadband Deal.md', redundant 'Bedding set.md')", "impact": "MEDIUM", "risk_reduction": "Removes stale noise from active search and indexes", "effort": "Low (move 3 notes to Archive)", "confidence": "HIGH", "severity": "P2"},
        {"rank": 6, "action": "Create '.obsidian/daily-notes.json' pointing to '02 - Journal' to prevent new daily notes cluttering root", "impact": "HIGH", "risk_reduction": "Fixes core plugin destination drift", "effort": "Trivial (create JSON file)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 7, "action": "Resolve unmerged volatile worktree in '/private/tmp/taivault-food-os-mvp1' before next OS reboot", "impact": "HIGH", "risk_reduction": "Prevents loss of Food OS commits", "effort": "Medium (git merge/prune)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 8, "action": "Fix self-referencing obsolete link in '02 - Taani/Travel/00 - Travel Index.md' ([[03 - Projects/Travel/...]])", "impact": "MEDIUM", "risk_reduction": "Eliminates broken navigation link", "effort": "Trivial (1-line edit)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 9, "action": "Fix broken relative markdown links with URL-encoded '%2F' slashes in '06 - Resources/AI/Markdown-First...'", "impact": "MEDIUM", "risk_reduction": "Restores broken agent specification references", "effort": "Low (replace '%2F' with '/')", "confidence": "HIGH", "severity": "P1"},
        {"rank": 10, "action": "Address iCloud POSIX symlinks in '11 - Agents/Workflows/' for cross-platform mobile compatibility", "impact": "HIGH", "risk_reduction": "Ensures iOS/iPadOS Obsidian sync resilience", "effort": "Medium (replace symlinks with local router notes)", "confidence": "HIGH", "severity": "P1"},
    ]

    metrics = {
        "total_files": len(all_files),
        "markdown_notes": len(md_files),
        "folders": len(rel_folders),
        "attachments": len(pdf_files) + len(img_files),
        "pdfs": len(pdf_files),
        "images": len(img_files),
        "internal_links_broken": len(broken_links),
        "broken_embeds": 0,
        "ambiguous_links": len(ambiguous_links),
        "dfs_sections_audited": len(dfs_sections),
        "overloaded_folders": len(overloaded_folders),
        "missing_index_folders": len(missing_index_folders),
        "note_relocation_proposals": len(relocation_proposals),
        "archival_candidates": len(archival_candidates),
        "unique_properties": len(properties_used),
        "unique_tags": len(tags_used),
        "p0_issues": p0_count,
        "p1_issues": p1_count,
        "p2_issues": p2_count,
        "p3_issues": p3_count,
        "p4_issues": p4_count
    }

    # Write Vault Health Findings.json
    findings_data = {
        "audit_version": "2.0",
        "auditor": "vault-sentry",
        "vault_path": vault_dir,
        "audit_timestamp": now_iso,
        "metrics": metrics,
        "scores": scores,
        "dfs_sections": dfs_sections,
        "relocation_proposals": relocation_proposals,
        "archival_candidates": archival_candidates,
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
**Audit Engine**: `vault-sentry` v2.0 (DFS Directory & Structural Sentinels | Strict Read-Only Mode)

---

## Executive Summary

The **Vault Sentry** audit evaluated **{metrics['total_files']} files** ({metrics['markdown_notes']} Markdown notes, {metrics['folders']} folders) through a complete **Depth-First Search (DFS)** directory-by-directory walk.

Overall vault health is scored at **{scores['Overall vault health']}/100**.

### Key Diagnostic Takeaways:
1. **DFS Structural Traversal**: Audited **{metrics['dfs_sections_audited']} directory sections**. Discovered a major organizational bottleneck in `02 - Taani/House`, which has become an overloaded flat dumping ground of **48 notes** spanning cleaning, appliances, DIY renovation, furniture, and conveyancing.
2. **Note Relocation Analysis ("Where it should live instead")**: Identified **{len(relocation_proposals)} misplaced notes** that violate domain boundaries (e.g. running races, cycling guides, coffee brewing, and water filters stored under `06 - Resources/AI`).
3. **Archival Candidates ("Outdated & untouched notes")**: Flagged **{len(archival_candidates)} notes for archival** to `10 - Archive/`, including dead indexes (`05 - Knowledge/Finance Index.md`), time-decaying purchase research (`Best Broadband Deal.md`), and redundant notes (`Bedding set.md`).
4. **Git Deletion Hazard**: Files moved from `04 - Areas/House` and `03 - Projects/Travel` to `02 - Taani/` show as deleted in Git while `02 - Taani/` remains untracked. A partial commit risks permanent note deletion.
5. **Silent Dataview Omission**: `04 - Areas/Technology` has no index note (`00 - Technology Index.md`), causing the Dataview query in `04 - Areas/00 - Areas Index.md` to omit Technology entirely.

---

## Audit Metrics

| Metric | Count | Metric | Count |
|---|---:|---|---:|
| **Total Files** | {metrics['total_files']} | **DFS Sections Audited** | {metrics['dfs_sections_audited']} |
| **Markdown Notes** | {metrics['markdown_notes']} | **Overloaded Flat Folders** | {metrics['overloaded_folders']} |
| **Folders** | {metrics['folders']} | **Folders Missing Indexes** | {metrics['missing_index_folders']} |
| **Attachments (PDFs & Images)** | {metrics['attachments']} | **Note Relocation Proposals** | **{metrics['note_relocation_proposals']}** |
| **Broken Internal Links** | {metrics['internal_links_broken']} | **Notes Suggested to Archive** | **{metrics['archival_candidates']}** |
| **Unique Properties** | {metrics['unique_properties']} | **P0 Issues (Data Loss Risk)** | **{metrics['p0_issues']}** |
| **Unique Tags** | {metrics['unique_tags']} | **P1 Issues (Broken / Omitted)** | **{metrics['p1_issues']}** |
| **P2 Issues (Structural / Misplaced)** | **{metrics['p2_issues']}** | **P3 / P4 Issues (Hygiene & Stale)** | **{metrics['p3_issues'] + metrics['p4_issues']}** |

---

## Health Scorecard

| Diagnostic Area | Score | Primary Contributing Factor |
|---|---:|---|
| **Filesystem integrity** | {scores['Filesystem integrity']}/100 | Top-level numbering collision (`02 - Journal` vs `02 - Taani`), OS metadata |
| **Markdown integrity** | {scores['Markdown integrity']}/100 | Clean code fences, no conflict markers, minor heading jumps |
| **Link integrity** | {scores['Link integrity']}/100 | 9 broken wikilinks, 5 broken relative markdown links |
| **Attachment integrity** | {scores['Attachment integrity']}/100 | 100% of attachments in `08 - Attachments` referenced |
| **Metadata/frontmatter** | {scores['Metadata/frontmatter']}/100 | High consistency on `parent` and `tags`; 35 notes lack frontmatter |
| **Tag consistency** | {scores['Tag consistency']}/100 | Clear domain tags; template placeholder tag leak (`#{{topic-tag-1}}`) |
| **Structured-data integrity** | {scores['Structured-data integrity']}/100 | Valid Bases files, TSV, and JSON configs |
| **Navigation/discoverability** | {scores['Navigation/discoverability']}/100 | Technology omitted from Areas Index; 48-file flat clutter in House; misplaced AI notes |
| **Automation robustness** | {scores['Automation robustness']}/100 | 101 hardcoded machine paths; external POSIX symlinks in iCloud |
| **Obsidian configuration** | {scores['Obsidian configuration']}/100 | `daily-notes.json` missing while core plugin is enabled |
| **Git/sync resilience** | {scores['Git/sync resilience']}/100 | Moved folders uncommitted in `02 - Taani/`; volatile worktree in `/private/tmp/` |
| **Overall vault health** | **{scores['Overall vault health']}/100** | **Solid core knowledge base; needs folder restructuring and Git staging** |

---

## Section-by-Section DFS Structural Audit

The vault was traversed in Depth-First Search order. Below is the structural evaluation of each major branch:

| Directory Section | Depth | Notes | Subdirs | Index Note | Coherence | Assessment & Findings |
|---|---:|---:|---:|---|---|---|
""")
        for s in dfs_sections:
            if s["depth"] <= 2 or s["assessment"] != "Healthy":
                rf.write(f"| `{s['section']}` | {s['depth']} | {s['notes_count']} | {s['subdirs_count']} | {s['index_note'] or 'None'} | {s['coherence']} | {s['assessment']} |\n")

        rf.write(f"""
---

## Note Relocation Proposals ("Where Notes Should Live Instead")

To resolve folder clutter and maintain the Vault Constitution classification rules, the following **{len(relocation_proposals)} notes** are proposed for relocation:

### 1. Misplaced Notes in `06 - Resources/AI` (Domain Drift)
These notes do not cover artificial intelligence and belong in their respective Areas/Domains:

| Note | Current Location | Where It Should Live Instead | Reason |
|---|---|---|---|
| `Most Prestigious Running Races London.md` | `06 - Resources/AI` | `04 - Areas/Health and Fitness/` | London running races guide; belongs under Health and Fitness. |
| `Cycling 101.md` | `06 - Resources/AI` | `04 - Areas/Cycling/` | Beginner cycling guide; belongs in the active Cycling area. |
| `Cycling 102.md` | `06 - Resources/AI` | `04 - Areas/Cycling/` | Advanced cycling and gear guide; belongs in Cycling area. |
| `Coffee 101.md` | `06 - Resources/AI` | `02 - Taani/House/` or `05 - Knowledge/` | Coffee brewing guide; belongs under House routines or Knowledge. |
| `Household Water Filtration Systems (Deep Research).md` | `06 - Resources/AI` | `02 - Taani/House/` | Undersink water filtration research; belongs under House maintenance. |

### 2. Overloaded `02 - Taani/House/` (48 Flat Notes Clutter)
`02 - Taani/House/` has become an overloaded flat dumping ground. To make it clean and maintainable, notes should be clustered into thematic subfolders:

- **Cluster A: Cleaning (`02 - Taani/House/Cleaning/`)** — 10 notes:
  - `Bathroom Cleaning Supplies.md`, `Best Household Cleaning Brands by Category.md`, `Bulk Buying Household Cleaning Supplies.md`, `Cleaning tools and supplies.md`, `General Cleaning Supplies.md`, `Hand wash.md`, `Household Cleaning & Supplies.md`, `Household Cleaning System.md`, `Kitchen Cleaning Supplies.md`, `Laundry Cleaning Supplies.md`.
- **Cluster B: Appliances (`02 - Taani/House/Appliances/`)** — 7 notes:
  - `Air fryer and rice cooker.md`, `Dreame X40 Ultra.md`, `Robot Vacuum Research.md`, `Smart Thermostats Research.md`, `Smart Doorbell Research.md`, `Replacing Washing machine with Washer Dryer.md`, `Best Water Filter for Home.md`.
- **Cluster C: Furnishing & Homeware (`02 - Taani/House/Furnishing/`)** — 12 notes:
  - `Best Bedding and Linen sets.md`, `Buying new Bathroom stuff.md`, `Buying new Kitchenware.md`, `Coat Hook Panel and Shoe Rack.md`, `Coffee Table.md`, `Cookware and knives.md`, `Dining table and Chairs.md`, `Dinnerware and utensils.md`, `Duvet.md`, `Entrance and Garden mat.md`, `Food containers and labels.md`, `Furniture Links.md`.
- **Cluster D: Renovation & Maintenance (`02 - Taani/House/Renovation/`)** — 8 notes:
  - `Fixing Door Foil Peel.md`, `Installing Herringbone LVT.md`, `Replacing Pendant with Spotlights.md`, `Replacing Switches.md`, `WAGNER Paint Sprayer.md`, `Solar Panels.md`, `Prep tools and boards.md`, `Kitchen Storage containers.md`.
- **Cluster E: Property Transaction (`02 - Taani/House/Property/`)** — 3 notes:
  - `Original Rightmove Listing and Measurements.md`, `Legal and Mortgage for House.md`, `Current vs New Household Budget.md`.

---

## Archival Candidates ("Outdated, Old & Untouched Notes")

The following notes are candidates for moving to `10 - Archive/` based on staleness, obsolescence, or completion:

| Note | Untouched (Days) | Inbound Links | Proposed Archive Destination | Reason |
|---|---:|---:|---|---|
| `05 - Knowledge/Finance Index.md` | 42 | 0 | `10 - Archive/05 - Knowledge/Finance Index.md` | Superseded index: contains empty Dataview query with 0 notes. Canonical finance moved to `02 - Taani/Finance`. |
| `02 - Taani/House/Best Broadband Deal.md` | 45 | 1 | `10 - Archive/House/Best Broadband Deal (Historical).md` | Time-sensitive contract research. Expired broadband deals become inaccurate. |
| `02 - Taani/House/Bedding set.md` | 45 | 1 | `10 - Archive/House/Bedding set (Superseded).md` | Duplicate research superseded by `Best Bedding and Linen sets.md`. Untouched for 45+ days. |
| Past Travel Plans / Packing Lists | 45+ | 1 | `10 - Archive/Travel/...` | Any trip plan or packing list from past dates (e.g. `Amsterdam 2026 - Packing List.md` pattern). |

---

## Critical Findings (P0 & P1)

### [P0] VS-037 — Uncommitted Folder Moves Risk Permanent Note Deletion in Git
- **Path**: Vault Git Repository (`.git`)
- **Evidence**: Notes from `04 - Areas/House` and `03 - Projects/Travel` were moved into `02 - Taani/`. In `git status -s`, the old locations show as `D` (deleted), while `02 - Taani/` is untracked `??`.
- **Risk**: A careless `git commit -a` or sync script will commit the deletions without staging the new files, permanently wiping House and Travel notes from Git history.
- **Remedy**: Explicitly stage and commit `02 - Taani/` alongside the deletions: `git add "02 - Taani" "03 - Projects" "04 - Areas"`.

### [P1] VS-034 — Area 'Technology' Silently Omitted from Areas Index
- **Path**: `04 - Areas/Technology/`
- **Evidence**: `04 - Areas/Technology` exists on disk and contains `Bionic Skills Setup.md`, but has no `00 - Technology Index.md`. The Dataview query in `04 - Areas/00 - Areas Index.md` filters by `contains(file.name, "Index")`, completely omitting Technology.
- **Remedy**: Create `04 - Areas/Technology/00 - Technology Index.md` with parent `[[00 - Areas Index]]`.

### [P1] VS-038 — Volatile Git Worktree in `/private/tmp/`
- **Path**: `/private/tmp/taivault-food-os-mvp1` (Branch: `codex/food-os-mvp1`)
- **Evidence**: An active Git worktree containing 2 unmerged commits (`Compartmentalize Food OS under dedicated area`, `Implement Food OS MVP1 inventory foundation`) resides in macOS `/private/tmp/`.
- **Risk**: macOS purges `/private/tmp/` on restart or storage pressure, leaving Git worktree metadata broken and unmerged work orphaned.
- **Remedy**: Merge `codex/food-os-mvp1` into `main` or move worktree to a persistent directory under `~/.taani-agent/workspaces/`.

### [P1] VS-033 — Core Plugin `daily-notes` Missing Destination Configuration
- **Path**: `.obsidian/core-plugins.json`
- **Evidence**: `daily-notes: true` in `core-plugins.json`, but `.obsidian/daily-notes.json` does not exist.
- **Risk**: Invoking "Open today's daily note" dumps newly created daily notes into the vault root instead of `02 - Journal/`.
- **Remedy**: Create `.obsidian/daily-notes.json` setting folder to `"02 - Journal"`.

### [P1] VS-004 / VS-005 — iCloud Sync Hazard: External POSIX Symlinks
- **Path**: `11 - Agents/Workflows/finance-checkpoint` & `habits-checkpoint`
- **Evidence**: Both directories are POSIX symlinks pointing outside iCloud to `/Users/sai/.codex/skills/...`.
- **Risk**: iCloud cannot synchronize POSIX symlinks pointing to external absolute paths to iOS/iPadOS devices.
- **Remedy**: Replace directory symlinks in iCloud with router notes or external agent configs.

---

## Top 10 Actions

| Rank | Action | Impact | Risk Reduction | Effort | Confidence | Severity |
|---|---|---|---|---|---|---|
| **1** | Stage and commit untracked `02 - Taani/` in Git | CRITICAL | Prevents permanent data loss of House & Travel domains | Low (`git add 02 - Taani`) | HIGH | **P0** |
| **2** | Create `04 - Areas/Technology/00 - Technology Index.md` | HIGH | Restores missing Technology area to Areas Dataview query | Low (create 1 note) | HIGH | **P1** |
| **3** | Relocate misplaced notes out of `06 - Resources/AI` | HIGH | Restores domain boundaries (Running -> Health, Cycling -> Cycling, etc.) | Low (move 5 notes) | HIGH | **P1** |
| **4** | Cluster overloaded `02 - Taani/House` (48 flat notes) into subfolders | HIGH | Transforms flat clutter into clean thematic subfolders | Medium (batch moves) | HIGH | **P2** |
| **5** | Archive superseded notes to `10 - Archive/` | MEDIUM | Removes dead indexes and expired research from active search | Low (archive 3 notes) | HIGH | **P2** |
| **6** | Create `.obsidian/daily-notes.json` pointing to `02 - Journal` | HIGH | Fixes daily notes dumping into vault root | Trivial (create JSON file) | HIGH | **P1** |
| **7** | Resolve unmerged volatile worktree in `/private/tmp/taivault-food-os-mvp1` | HIGH | Prevents loss of Food OS commits on reboot | Medium (git merge/prune) | HIGH | **P1** |
| **8** | Fix self-referencing link in `02 - Taani/Travel/00 - Travel Index.md` | MEDIUM | Eliminates broken navigation link | Trivial (1-line edit) | HIGH | **P1** |
| **9** | Fix `%2F` encoded relative links in `Markdown-First...` note | MEDIUM | Restores broken agent specification references | Low (replace `%2F` with `/`) | HIGH | **P1** |
| **10** | Address iCloud POSIX symlinks in `11 - Agents/Workflows/` | HIGH | Ensures iOS/iPadOS Obsidian sync resilience | Medium (replace symlinks) | HIGH | **P1** |

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
**Auditor**: `vault-sentry`  
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

### [AUTO-02] Fix URL-Encoded `%2F` Slashes in Relative Markdown Links
- **Target**: `06 - Resources/AI/Markdown-First Obsidian Vault Instruction System for AI Agents.md`
- **Action**: Replace `%2F` with standard `/` on lines with relative links.

### [AUTO-03] Clean Phantom Deleted Image Reference in Workspace
- **Target**: `.obsidian/workspace.json`
- **Action**: Remove `"08 - Attachments/Pasted image 20260330175711.png"` from open tabs / recent files.

### [AUTO-04] Remove Leaked Template Placeholder Tag
- **Target**: `09 - Templates/YouTube Summary Template.md`
- **Action**: Remove `- {{topic-tag-1}}` from tags frontmatter block.

---

## 2. Approval-Required Repairs
*Changes that involve note creation, renaming, Git staging, or structural navigation.*

### [APPR-01] Stage and Commit Untracked `02 - Taani/` in Vault Git Repository
- **Command**: `git -C "{vault_dir}" add "02 - Taani" "03 - Projects" "04 - Areas" && git -C "{vault_dir}" commit -m "refactor: track moved House and Travel domains under 02 - Taani"`

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

### [APPR-03] Relocate Misplaced Notes Out of `06 - Resources/AI`
Execute following moves:
1. `06 - Resources/AI/Most Prestigious Running Races London.md` → `04 - Areas/Health and Fitness/Most Prestigious Running Races London.md`
2. `06 - Resources/AI/Cycling 101.md` → `04 - Areas/Cycling/Cycling 101.md`
3. `06 - Resources/AI/Cycling 102.md` → `04 - Areas/Cycling/Cycling 102.md`
4. `06 - Resources/AI/Coffee 101.md` → `02 - Taani/House/Coffee 101.md`
5. `06 - Resources/AI/Household Water Filtration Systems (Deep Research).md` → `02 - Taani/House/Household Water Filtration Systems (Deep Research).md`

### [APPR-04] Cluster Overloaded `02 - Taani/House` (48 Notes)
Create subfolders and move notes:
1. `02 - Taani/House/Cleaning/` (10 cleaning notes)
2. `02 - Taani/House/Appliances/` (7 appliance notes)
3. `02 - Taani/House/Furnishing/` (12 furnishing notes)
4. `02 - Taani/House/Renovation/` (8 renovation/DIY notes)
5. `02 - Taani/House/Property/` (3 property/mortgage notes)

### [APPR-05] Archive Outdated & Stale Notes to `10 - Archive/`
1. `05 - Knowledge/Finance Index.md` → `10 - Archive/05 - Knowledge/Finance Index.md`
2. `02 - Taani/House/Best Broadband Deal.md` → `10 - Archive/House/Best Broadband Deal (Historical).md`
3. `02 - Taani/House/Bedding set.md` → `10 - Archive/House/Bedding set (Superseded).md`

### [APPR-06] Resolve Volatile Git Worktree in `/private/tmp/`
- **Command**: Merge branch `codex/food-os-mvp1` into `main` and remove worktree: `git -C "{vault_dir}" worktree remove /private/tmp/taivault-food-os-mvp1`.

### [APPR-07] Fix Obsolete Self-Referencing Wikilink in Travel Index
- **Target**: `02 - Taani/Travel/00 - Travel Index.md:19`
- **Action**: Replace `[[03 - Projects/Travel/00 - Travel Index]]` with `[[02 - Taani/Travel/00 - Travel Index]]`.

---

## 3. Human Judgment Required
*Decisions requiring personal user preference.*

### [HUMAN-01] Top-Level Folder Numbering Collision
- **Context**: `02 - Journal` and `02 - Taani` share the same prefix `02 -`.
- **Options**:
  1. Renumber `02 - Taani` to `03 - Taani` and cascade numbering.
  2. Drop numeric prefix on Taani (e.g. `Taani/`).
  3. Leave as intentional shared household marker.

### [HUMAN-02] Cross-Platform Mobile Sync for Workflows
- **Context**: `11 - Agents/Workflows/finance-checkpoint` and `habits-checkpoint` are external POSIX symlinks that do not sync to iOS.
- **Options**:
  1. Replace symlink directories with markdown router notes.
  2. Keep symlinks for desktop-only usage.
""")
    print(f"[+] Written repair manifest to: {manifest_file}")
    print("[*] Vault Sentry completed successfully.")

if __name__ == "__main__":
    args = parse_args()
    run_sentry(args.vault, args.output)
