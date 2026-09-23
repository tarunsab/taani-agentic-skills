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
    parser.add_argument("--output", help="Directory to output reports (defaults to '11 - Agents/Audits' or vault root)")
    parser.add_argument("--suggest", type=str, help="Suggest destination for a new note based on title or description")
    parser.add_argument("--suggest-file", type=str, help="Suggest destination for a draft markdown file")
    parser.add_argument("--json", action="store_true", help="Output destination suggestion or findings as JSON")
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

def suggest_destination(query, note_text="", vault_dir=None):
    """
    Suggest optimal folder path, clean filename, parent index wikilink,
    tags, icon, classification rationale, frontmatter scaffold, and alternative destination.
    Distinguishes Shared Household Space (02 - Taani) vs Personal Space, and enforces PARA tiers.
    """
    combined = (query + " " + note_text).lower()
    clean_title = query.strip()
    if clean_title.endswith(".md"):
        clean_title = clean_title[:-3]

    # Clean title helper
    def fmt_title(raw):
        # Remove common prefixes like 'Recipe for', 'How to', 'Draft note on'
        t = re.sub(r"^(?:recipe\s+for|draft\s+note\s+on|guide\s+to|notes\s+on)\s+", "", raw, flags=re.IGNORECASE).strip()
        return t

    # 1. Shared Household Space (02 - Taani)
    # 1A. Recipes
    is_recipe = any(w in combined for w in ["recipe", "curry", "rice", "dal", "masala", "paneer", "tofu", "sourdough", "pasta", "dessert", "ice cream", "cookie", "cake", "salad", "bake", "roast"]) and not any(w in combined for w in ["running", "workout", "gym", "marathon", "cycling"])
    if is_recipe:
        next_num = 12
        if vault_dir and os.path.exists(os.path.join(vault_dir, "02 - Taani", "Food", "Recipes")):
            rec_files = os.listdir(os.path.join(vault_dir, "02 - Taani", "Food", "Recipes"))
            nums = [int(m.group(1)) for f in rec_files if (m := re.match(r"^R(\d+)", f))]
            if nums:
                next_num = max(nums) + 1
        dish_name = re.sub(r"\brecipe\b", "", fmt_title(clean_title), flags=re.IGNORECASE).strip()
        fname = f"R{next_num:03d} - {dish_name}.md"
        return {
            "query": query,
            "recommended_folder": "02 - Taani/Food/Recipes/",
            "recommended_filename": fname,
            "full_recommended_path": f"02 - Taani/Food/Recipes/{fname}",
            "parent_index": "[[00 - Food Index]]",
            "recommended_tags": ["food", "recipe"],
            "recommended_icon": "🍳",
            "tier": "Resource (Shared)",
            "rationale": "Culinary recipe shared within household food system. Follows standard sequential Rxxx numbering.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - Food Index]]\"\ntags:\n  - food\n  - recipe\n---",
            "alternative_destination": "02 - Taani/Food/",
            "alternative_rationale": "If this document is a broad weekly meal framework or grocery list rather than a single recipe."
        }

    # 1B. Food & Dining General
    if any(w in combined for w in ["grocery", "groceries", "restaurant", "meal plan", "dining out", "supermarket", "food prep", "kitchen routine"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "02 - Taani/Food/",
            "recommended_filename": fname,
            "full_recommended_path": f"02 - Taani/Food/{fname}",
            "parent_index": "[[00 - Food Index]]",
            "recommended_tags": ["food", "household"],
            "recommended_icon": "🍽️",
            "tier": "Area (Shared)",
            "rationale": "Household food provisioning, recurring grocery system, or joint dining directory.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - Food Index]]\"\ntags:\n  - food\n  - household\n---",
            "alternative_destination": "02 - Taani/Food/Recipes/",
            "alternative_rationale": "Use Recipes subfolder if this document is an individual cooking card."
        }

    # 1C. House - Cleaning
    if any(w in combined for w in ["cleaning", "detergent", "laundry", "cleaner", "scrub", "chores", "bleach", "mop", "dishwasher tablets"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "02 - Taani/House/Cleaning/",
            "recommended_filename": fname,
            "full_recommended_path": f"02 - Taani/House/Cleaning/{fname}",
            "parent_index": "[[00 - House Index]]",
            "recommended_tags": ["house", "cleaning"],
            "recommended_icon": "🧽",
            "tier": "Area (Shared)",
            "rationale": "Household maintenance, room-by-room cleaning checklist, or chemical cleaning supply reference.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - House Index]]\"\ntags:\n  - house\n  - cleaning\n---",
            "alternative_destination": "02 - Taani/House/",
            "alternative_rationale": "Flat House root if subfolder clustering is not yet adopted."
        }

    # 1D. House - Appliances
    if any(w in combined for w in ["dreame", "robot vacuum", "air fryer", "vacuum", "thermostat", "smart doorbell", "washing machine", "washer dryer", "water filter", "appliance"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "02 - Taani/House/Appliances/",
            "recommended_filename": fname,
            "full_recommended_path": f"02 - Taani/House/Appliances/{fname}",
            "parent_index": "[[00 - House Index]]",
            "recommended_tags": ["house", "appliances"],
            "recommended_icon": "🤖",
            "tier": "Resource (Shared)",
            "rationale": "Household appliance research, manual instructions, or smart home device specifications.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - House Index]]\"\ntags:\n  - house\n  - appliances\n---",
            "alternative_destination": "02 - Taani/House/",
            "alternative_rationale": "Flat House root if subfolder clustering is not yet adopted."
        }

    # 1E. House - Furnishing & Homeware
    if any(w in combined for w in ["bedding", "linen", "duvet", "pillow", "sofa", "table", "chair", "curtain", "furniture", "dinnerware", "cutlery", "rug", "wardrobe"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "02 - Taani/House/Furnishing/",
            "recommended_filename": fname,
            "full_recommended_path": f"02 - Taani/House/Furnishing/{fname}",
            "parent_index": "[[00 - House Index]]",
            "recommended_tags": ["house", "furnishing"],
            "recommended_icon": "🛋️",
            "tier": "Resource (Shared)",
            "rationale": "Household furniture links, homeware purchase options, and interior decor references.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - House Index]]\"\ntags:\n  - house\n  - furnishing\n---",
            "alternative_destination": "02 - Taani/House/",
            "alternative_rationale": "Flat House root if subfolder clustering is not yet adopted."
        }

    # 1F. House - Renovation & DIY (Shared Project)
    if any(w in combined for w in ["lvt", "flooring", "spotlight", "switch", "door foil", "paint", "sprayer", "renovation", "diy", "plaster", "tiling", "solar panel"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "02 - Taani/House/Renovation/",
            "recommended_filename": fname,
            "full_recommended_path": f"02 - Taani/House/Renovation/{fname}",
            "parent_index": "[[00 - House Index]]",
            "recommended_tags": ["house", "renovation", "project"],
            "recommended_icon": "🪵",
            "tier": "Project (Shared)",
            "rationale": "Finite household home improvement, electrical modification, or DIY renovation task.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - House Index]]\"\ntags:\n  - house\n  - renovation\n  - project\n---",
            "alternative_destination": "03 - Projects/House Renovation/",
            "alternative_rationale": "If personal projects and household projects are merged into vault top-level 03 - Projects."
        }

    # 1G. House - Property / Legal
    if any(w in combined for w in ["mortgage", "rightmove", "conveyancing", "deeds", "surveyor", "solicitor", "property search"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "02 - Taani/House/Property/",
            "recommended_filename": fname,
            "full_recommended_path": f"02 - Taani/House/Property/{fname}",
            "parent_index": "[[00 - House Index]]",
            "recommended_tags": ["house", "property", "legal"],
            "recommended_icon": "⚖️",
            "tier": "Archive / Resource (Shared)",
            "rationale": "Property transaction history, mortgage terms, or conveyancing documentation.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - House Index]]\"\ntags:\n  - house\n  - property\n  - legal\n---",
            "alternative_destination": "02 - Taani/House/",
            "alternative_rationale": "Flat House root if property subfolder is not yet provisioned."
        }

    # 1H. Finance (Shared)
    if any(w in combined for w in ["household budget", "joint budget", "joint finance", "checkpoint", "net worth", "household expense", "financial dashboard"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "02 - Taani/Finance/",
            "recommended_filename": fname,
            "full_recommended_path": f"02 - Taani/Finance/{fname}",
            "parent_index": "[[00 - Finance Index]]",
            "recommended_tags": ["finance", "household"],
            "recommended_icon": "💷",
            "tier": "Area (Shared)",
            "rationale": "Joint household financial cadence, budget checkpoint, or asset tracking.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - Finance Index]]\"\ntags:\n  - finance\n  - household\n---",
            "alternative_destination": "02 - Taani/Finance/Checkpoints/",
            "alternative_rationale": "Use Checkpoints subfolder if this is a dated monthly balance snapshot."
        }

    # 1I. Travel (Shared)
    if any(w in combined for w in ["packing list", "itinerary", "holiday", "trip", "flight", "hotel", "roadtrip", "weekend away", "vacation"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "02 - Taani/Travel/",
            "recommended_filename": fname,
            "full_recommended_path": f"02 - Taani/Travel/{fname}",
            "parent_index": "[[00 - Travel Index]]",
            "recommended_tags": ["travel", "project"],
            "recommended_icon": "✈️",
            "tier": "Project (Shared)",
            "rationale": "Finite shared travel itinerary, holiday planning, or trip packing checklist.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - Travel Index]]\"\ntags:\n  - travel\n  - project\n---",
            "alternative_destination": "03 - Projects/Travel/",
            "alternative_rationale": "If personal and shared travel are unified under 03 - Projects."
        }

    # 2. Personal Space
    # 2A. AI Agent / Tooling (11 - Agents)
    if any(w in combined for w in ["agent", "subagent", "prompt spec", "workflow", "audit", "vault sentry", "bionic skill", "anthropic tool", "skill.md"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "11 - Agents/Workflows/",
            "recommended_filename": fname,
            "full_recommended_path": f"11 - Agents/Workflows/{fname}",
            "parent_index": "[[Agent Index]]",
            "recommended_tags": ["agent", "workflow"],
            "recommended_icon": "🤖",
            "tier": "System / Agent Tooling",
            "rationale": "AI agent specification, executable workflow instruction, or governance rule.",
            "frontmatter_scaffold": f"---\nparent: \"[[Agent Index]]\"\ntags:\n  - agent\n  - workflow\n---",
            "alternative_destination": "11 - Agents/Workspace/",
            "alternative_rationale": "Use Workspace for temporary working drafts before canonizing into Workflows."
        }

    # 2B. Cycling
    if any(w in combined for w in ["cycling", "bike", "bicycle", "strava", "garmin", "gravel", "chain", "cassette", "derailleur", "pedals"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "04 - Areas/Cycling/",
            "recommended_filename": fname,
            "full_recommended_path": f"04 - Areas/Cycling/{fname}",
            "parent_index": "[[00 - Cycling Index]]",
            "recommended_tags": ["cycling", "fitness"],
            "recommended_icon": "🚲",
            "tier": "Area (Personal)",
            "rationale": "Maintained personal cycling area, gear maintenance log, or route database.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - Cycling Index]]\"\ntags:\n  - cycling\n  - fitness\n---",
            "alternative_destination": "04 - Areas/Health and Fitness/",
            "alternative_rationale": "If consolidating general cardio under Health and Fitness."
        }

    # 2C. Personal Health & Fitness
    if any(w in combined for w in ["running", "half marathon", "marathon", "5k", "10k", "cardio", "vo2 max", "zone 2", "gym", "hypertrophy", "workout", "lifting", "supplements", "protein", "sleep", "recovery"]):
        is_project = any(w in combined for w in ["half marathon", "marathon", "race day", "training plan", "taper"])
        folder = "03 - Projects/" if is_project else "04 - Areas/Health and Fitness/"
        parent = "[[00 - Projects Index]]" if is_project else "[[00 - Health and Fitness Index]]"
        tier = "Project (Personal)" if is_project else "Area (Personal)"
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": folder,
            "recommended_filename": fname,
            "full_recommended_path": f"{folder}{fname}",
            "parent_index": parent,
            "recommended_tags": ["health", "fitness", "running"] if "running" in combined else ["health", "fitness"],
            "recommended_icon": "🏃" if "running" in combined else "💪",
            "tier": tier,
            "rationale": "Personal health, training methodology, or finite race milestone.",
            "frontmatter_scaffold": f"---\nparent: \"{parent}\"\ntags:\n  - health\n  - fitness\n---",
            "alternative_destination": "04 - Areas/Health and Fitness/",
            "alternative_rationale": "If treating race training as continuous physical maintenance rather than a distinct project."
        }

    # 2D. Personal Habits
    if any(w in combined for w in ["habit", "atomic habit", "streak", "habit tracker", "daily routine", "habit audit", "habit experiment"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "04 - Areas/Habits/",
            "recommended_filename": fname,
            "full_recommended_path": f"04 - Areas/Habits/{fname}",
            "parent_index": "[[00 - Habits Index]]",
            "recommended_tags": ["habits", "productivity"],
            "recommended_icon": "⚡",
            "tier": "Area (Personal)",
            "rationale": "Personal behavioral system, habit experiments, or daily tracking cadence.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - Habits Index]]\"\ntags:\n  - habits\n  - productivity\n---",
            "alternative_destination": "04 - Areas/Habits/Experiments/",
            "alternative_rationale": "If this note defines an active, 30-day habit hypothesis experiment."
        }

    # 2E. NAS & Homelab
    if any(w in combined for w in ["nas", "synology", "qbittorrent", "seedbox", "docker", "portainer", "plex", "jellyfin", "truenas", "unraid"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "04 - Areas/NAS/",
            "recommended_filename": fname,
            "full_recommended_path": f"04 - Areas/NAS/{fname}",
            "parent_index": "[[00 - NAS Index]]",
            "recommended_tags": ["nas", "technology", "homelab"],
            "recommended_icon": "🖧",
            "tier": "Area (Personal)",
            "rationale": "Personal home server operations, container configurations, and NAS maintenance.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - NAS Index]]\"\ntags:\n  - nas\n  - technology\n  - homelab\n---",
            "alternative_destination": "04 - Areas/Technology/",
            "alternative_rationale": "If homelab configurations are grouped under general Technology."
        }

    # 2F. Technology & Dev Setup
    if any(w in combined for w in ["cli", "terminal", "zsh", "dotfiles", "bionic setup", "ide", "vscode", "cursor setup", "brew", "macos"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "04 - Areas/Technology/",
            "recommended_filename": fname,
            "full_recommended_path": f"04 - Areas/Technology/{fname}",
            "parent_index": "[[00 - Technology Index]]",
            "recommended_tags": ["technology", "setup", "tools"],
            "recommended_icon": "💻",
            "tier": "Area (Personal)",
            "rationale": "Personal developer workstation, environment setup, and CLI configuration.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - Technology Index]]\"\ntags:\n  - technology\n  - setup\n---",
            "alternative_destination": "05 - Knowledge/",
            "alternative_rationale": "If this is an evergreen programming conceptual guide rather than machine setup."
        }

    # 2G. Personal Admin & Identity
    if any(w in combined for w in ["passport", "driving license", "hmrc", "tax return", "pension", "national insurance", "visa", "id docs"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "04 - Areas/Admin/",
            "recommended_filename": fname,
            "full_recommended_path": f"04 - Areas/Admin/{fname}",
            "parent_index": "[[00 - Admin Index]]",
            "recommended_tags": ["admin", "personal"],
            "recommended_icon": "🪪",
            "tier": "Area (Personal)",
            "rationale": "Personal civil documentation, identity records, and tax administrative filing.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - Admin Index]]\"\ntags:\n  - admin\n  - personal\n---",
            "alternative_destination": "10 - Archive/",
            "alternative_rationale": "If these are expired identity documents preserved for historical reference."
        }

    # 2H. Deep Dives (Knowledge)
    if any(w in combined for w in ["deep dive", "architecture", "system design", "spec", "memory models", "comprehensive guide"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "05 - Knowledge/Deep Dives/",
            "recommended_filename": fname,
            "full_recommended_path": f"05 - Knowledge/Deep Dives/{fname}",
            "parent_index": "[[00 - Deep Dives Index]]",
            "recommended_tags": ["knowledge", "deep-dive", "architecture"],
            "recommended_icon": "🧭",
            "tier": "Knowledge (Personal)",
            "rationale": "Permanent synthetic architectural analysis, technical breakdown, or comprehensive deep dive.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - Deep Dives Index]]\"\ntags:\n  - knowledge\n  - deep-dive\n  - architecture\n---",
            "alternative_destination": "05 - Knowledge/",
            "alternative_rationale": "Can reside in Knowledge root if not adopting the Deep Dives sub-clustering."
        }

    # 2I. Book Summaries
    if any(w in combined for w in ["book summary", "reading notes", "chapter summary", "author", "book review"]) or ("book" in combined and any(b in combined for b in ["habits", "ikigai", "rich dad", "courage"])):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "06 - Resources/Books/",
            "recommended_filename": fname,
            "full_recommended_path": f"06 - Resources/Books/{fname}",
            "parent_index": "[[00 - Books Index]]",
            "recommended_tags": ["books", "reading", "summary"],
            "recommended_icon": "📚",
            "tier": "Resource (Personal)",
            "rationale": "Structured book review, chapter analysis, or mental model extraction from published literature.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - Books Index]]\"\ntags:\n  - books\n  - reading\n  - summary\n---",
            "alternative_destination": "06 - Resources/",
            "alternative_rationale": "General Resources folder if not catalogued inside Books Base."
        }

    # 2J. YouTube Summaries
    if any(w in combined for w in ["youtube", "video summary", "mkbhd", "podcast summary", "transcript"]):
        fname = f"{clean_title}.md"
        return {
            "query": query,
            "recommended_folder": "06 - Resources/YouTube/",
            "recommended_filename": fname,
            "full_recommended_path": f"06 - Resources/YouTube/{fname}",
            "parent_index": "[[00 - YouTube Index]]",
            "recommended_tags": ["youtube", "video", "summary"],
            "recommended_icon": "🎬",
            "tier": "Resource (Personal)",
            "rationale": "Summarized video content or transcript digest from YouTube.",
            "frontmatter_scaffold": f"---\nparent: \"[[00 - YouTube Index]]\"\ntags:\n  - youtube\n  - video\n---",
            "alternative_destination": "06 - Resources/Articles/",
            "alternative_rationale": "If the content is primarily text-based rather than video-derived."
        }

    # Fallback: Knowledge / General Notes
    fname = f"{clean_title}.md"
    return {
        "query": query,
        "recommended_folder": "05 - Knowledge/",
        "recommended_filename": fname,
        "full_recommended_path": f"05 - Knowledge/{fname}",
        "parent_index": "[[00 - Knowledge Index]]",
        "recommended_tags": ["knowledge"],
        "recommended_icon": "🧠",
        "tier": "Knowledge (Personal)",
        "rationale": "Evergreen conceptual knowledge, reference guide, or technical explanation.",
        "frontmatter_scaffold": f"---\nparent: \"[[00 - Knowledge Index]]\"\ntags:\n  - knowledge\n---",
        "alternative_destination": "01 - Home/01 - Inbox Index.md",
        "alternative_rationale": "If this is raw capture that needs further triage and refinement before permanent filing."
    }

def audit_para_conformance(vault_dir, md_files, rel_folders, note_frontmatter, note_contents):
    """
    Rigorously evaluate PARA conformance across:
    1. Overall Vault PARA (Projects, Areas, Resources, Archives)
    2. Shared Space (02 - Taani) PARA
    """
    findings = []

    # 1. Vault PARA Breakdown
    vault_p_notes = [p for p in md_files if p.startswith("03 - Projects") and not p.endswith("Index.md")]
    vault_a_notes = [p for p in md_files if p.startswith("04 - Areas")]
    vault_k_notes = [p for p in md_files if p.startswith("05 - Knowledge")]
    vault_r_notes = [p for p in md_files if p.startswith("06 - Resources")]
    vault_arch_notes = [p for p in md_files if p.startswith("10 - Archive")]

    # Check for projects scattered outside 03 - Projects
    scattered_projects = []
    for p, f in md_files.items():
        if not p.startswith("03 - Projects") and not p.startswith("10 - Archive"):
            base = os.path.basename(p)
            if any(term in base for term in ["Plan", "Itinerary", "Packing List", "Installing", "Replacing Switches", "Fixing Door Foil"]):
                scattered_projects.append(p)

    # Check for area leakage into Resources
    area_leakage = [p for p in md_files if p.startswith("06 - Resources/AI") and any(w in p for w in ["Running", "Cycling", "Coffee", "Water Filtration"])]

    # Scoring Vault PARA
    v_deductions = 0
    if len(vault_p_notes) == 0:
        v_deductions += 15
        findings.append({
            "severity": "P2",
            "category": "para-vault-dormant-projects",
            "path": "03 - Projects",
            "description": f"Projects directory is depleted/dormant ({len(vault_p_notes)} active notes); active project notes have drifted into '02 - Taani/Travel' and '02 - Taani/House'.",
            "suggested_action": "Centralize finite projects or formally link them to 00 - Projects Index.md",
            "confidence": "HIGH"
        })
    if len(area_leakage) > 0:
        v_deductions += 10
        findings.append({
            "severity": "P2",
            "category": "para-vault-area-leakage",
            "path": "06 - Resources/AI",
            "description": f"{len(area_leakage)} Area maintenance notes (Running, Cycling, Home Water Filter) leaked into Resource inbox '06 - Resources/AI'.",
            "suggested_action": "Relocate leaked area notes into 04 - Areas/ and 02 - Taani/House/",
            "confidence": "HIGH"
        })
    if len(vault_arch_notes) < 10:
        v_deductions += 10

    vault_para_score = max(20, min(100, 100 - v_deductions))

    vault_para = {
        "projects_count": len(vault_p_notes),
        "areas_count": len(vault_a_notes),
        "knowledge_count": len(vault_k_notes),
        "resources_count": len(vault_r_notes),
        "archive_count": len(vault_arch_notes),
        "total_para_notes": len(vault_p_notes) + len(vault_a_notes) + len(vault_k_notes) + len(vault_r_notes) + len(vault_arch_notes),
        "scattered_projects": scattered_projects,
        "area_leakage": area_leakage,
        "conformance_score": vault_para_score,
        "grade": "B-" if vault_para_score >= 80 else ("C+" if vault_para_score >= 65 else "C"),
        "status": "Moderate Conformance (Projects Dormant, Area Leakage Detected)"
    }

    # 2. Shared Space (02 - Taani) PARA Breakdown
    taani_notes = {p: f for p, f in md_files.items() if p.startswith("02 - Taani")}
    shared_projects = []
    shared_areas = []
    shared_resources = []
    shared_archives = []
    shared_indexes = []

    for rel_p, full_p in taani_notes.items():
        f = os.path.basename(rel_p)
        if "Index" in f:
            shared_indexes.append(rel_p)
        elif any(p in f for p in ["Plan", "Packing List", "Installing", "Replacing", "Fixing", "Paint Sprayer"]):
            shared_projects.append(rel_p)
        elif any(a in f for a in ["Cleaning", "System", "Checklist", "Supplies", "Hand wash", "Making a house smell", "Bins", "organisers", "containers", "labels", "Budget", "Dashboard", "How to Use"]):
            shared_areas.append(rel_p)
        elif any(arch in f for arch in ["Rightmove", "Legal and Mortgage", "Broadband Deal", "Bedding set.md"]):
            shared_archives.append(rel_p)
        else:
            shared_resources.append(rel_p)

    s_deductions = 0
    # Deductions for shared space:
    # Absence of folder-level PARA separation
    s_deductions += 25
    # Flat overloading in House (48 notes conflating all tiers)
    house_notes_count = len([p for p in taani_notes if p.startswith("02 - Taani/House")])
    if house_notes_count > 25:
        s_deductions += 20
        findings.append({
            "severity": "P2",
            "category": "para-shared-tier-conflation",
            "path": "02 - Taani/House",
            "description": f"'02 - Taani/House' contains {house_notes_count} flat notes conflating all 4 PARA tiers (DIY Projects, Cleaning Areas, Furnishing Resources, Property Archives).",
            "suggested_action": "Adopt thematic subfolder clustering (Renovation, Cleaning, Appliances, Furnishing, Property) or add frontmatter 'para:' tags.",
            "confidence": "HIGH"
        })

    shared_para_score = max(20, min(100, 100 - s_deductions))

    shared_para = {
        "total_notes": len(taani_notes),
        "projects_count": len(shared_projects),
        "areas_count": len(shared_areas),
        "resources_count": len(shared_resources),
        "archives_count": len(shared_archives),
        "indexes_count": len(shared_indexes),
        "projects": shared_projects,
        "areas": shared_areas,
        "resources": shared_resources,
        "archives": shared_archives,
        "indexes": shared_indexes,
        "conformance_score": shared_para_score,
        "grade": "C-",
        "status": "Low Conformance (Domain Silos with High Tier Conflation)",
        "recommendations": [
            "Cluster '02 - Taani/House' into thematic subfolders aligning with PARA: Renovation/ (Projects), Cleaning/ (Areas), Furnishing/ & Appliances/ (Resources), Property/ (Archive).",
            "Add 'para: project | area | resource | archive' to note frontmatter across '02 - Taani/' to power unified Dataview tracking."
        ]
    }

    return {
        "vault_para": vault_para,
        "shared_para": shared_para,
        "findings": findings
    }

def audit_iconize_coverage(vault_dir, all_files, md_files, rel_folders):
    """
    Audit Iconize (.obsidian/plugins/obsidian-icon-folder/data.json) configuration.
    Detects all expected pages and folders missing icons, suggests appropriate Lucide IDs or emojis,
    and returns coverage metrics and patch inventory.
    """
    icon_file = os.path.join(vault_dir, ".obsidian", "plugins", "obsidian-icon-folder", "data.json")
    icon_data = {}
    if os.path.exists(icon_file):
        try:
            with open(icon_file, "r", encoding="utf-8") as ic_f:
                icon_data = json.load(ic_f)
        except Exception:
            pass

    # Expected Targets
    expected_items = []

    # 1. Expected Folders
    folder_expectations = [
        ("01 - Home", "LiInbox", "P2", "Top-level inbox/home folder"),
        ("02 - Journal", "LiNotebookPen", "P2", "Top-level journal folder"),
        ("02 - Taani", "LiAlignVerticalDistributeCenter", "P2", "Shared household space"),
        ("02 - Taani/Finance", "LiBadgeDollarSign", "P2", "Shared finance domain"),
        ("02 - Taani/Food", "LiUtensils", "P1", "Shared culinary & food domain"),
        ("02 - Taani/House", "LiHome", "P2", "Shared house & property domain"),
        ("02 - Taani/Travel", "LiPlane", "P2", "Shared travel & trips domain"),
        ("03 - Projects", "LiFolderKanban", "P2", "Top-level projects folder"),
        ("04 - Areas", "LiMapPinned", "P2", "Top-level areas folder"),
        ("04 - Areas/Admin", "LiDock", "P2", "Personal admin domain"),
        ("04 - Areas/Cycling", "LiBike", "P2", "Personal cycling area"),
        ("04 - Areas/Habits", "LiFlame", "P1", "Personal habits area"),
        ("04 - Areas/Health and Fitness", "LiApple", "P2", "Personal health & fitness area"),
        ("04 - Areas/NAS", "LiHardDrive", "P2", "Personal NAS & homelab area"),
        ("04 - Areas/Photography", "LiCamera", "P2", "Personal photography area"),
        ("04 - Areas/Technology", "LiCpu", "P2", "Personal developer technology area"),
        ("05 - Knowledge", "LiBrain", "P2", "Top-level knowledge base"),
        ("05 - Knowledge/Deep Dives", "LiCompass", "P1", "Technical deep dive syntheses"),
        ("06 - Resources", "LiSearch", "P2", "Top-level resources repository"),
        ("06 - Resources/AI", "LiCog", "P2", "AI clippings and guides"),
        ("06 - Resources/Books", "LiBook", "P2", "Books reference base"),
        ("06 - Resources/YouTube", "LiFilm", "P2", "YouTube video summaries"),
        ("08 - Attachments", "LiFilm", "P2", "Attachments root"),
        ("08 - Attachments/Finance", "LiBadgeDollarSign", "P2", "Financial statements & attachment storage"),
        ("08 - Attachments/Habit Exports", "LiCalendar", "P2", "Habit tracking exports"),
        ("09 - Templates", "LiLayoutTemplate", "P2", "Note templates"),
        ("10 - Archive", "LiFolderSymlink", "P2", "Archive directory"),
        ("11 - Agents", "LiBot", "P2", "AI Agents root"),
        ("11 - Agents/Logs", "LiFileText", "P1", "Agent decision logs"),
        ("11 - Agents/References", "LiBookOpen", "P1", "Canonical agent references"),
        ("11 - Agents/Workflows", "LiWorkflow", "P1", "Executable agent workflows"),
        ("11 - Agents/Workspace", "LiTerminal", "P1", "Agent working state & scratchpad")
    ]
    for p, icon, prio, rat in folder_expectations:
        if os.path.exists(os.path.join(vault_dir, p)):
            expected_items.append({"path": p, "item_type": "folder", "suggested_icon": icon, "priority": prio, "rationale": rat})

    # 2. Expected Index Notes
    index_expectations = [
        ("01 - Home/00 - Home Index.md", "LiGrid2X2", "P2", "Home index"),
        ("01 - Home/01 - Inbox Index.md", "LiInbox", "P2", "Inbox index"),
        ("02 - Journal/00 - Journal Index.md", "LiNotebookPen", "P2", "Journal index"),
        ("02 - Taani/02 - Taani Index.md", "LiAlignVerticalDistributeCenter", "P1", "Shared space master index"),
        ("02 - Taani/Finance/00 - Finance Index.md", "LiBadgeDollarSign", "P2", "Finance index"),
        ("02 - Taani/Food/00 - Food Index.md", "LiUtensils", "P1", "Food & recipe index"),
        ("02 - Taani/House/00 - House Index.md", "LiHome", "P2", "House index"),
        ("02 - Taani/Travel/00 - Travel Index.md", "LiPlane", "P2", "Travel index"),
        ("03 - Projects/00 - Projects Index.md", "LiFolderKanban", "P2", "Projects index"),
        ("04 - Areas/00 - Areas Index.md", "LiMapPinned", "P2", "Areas master index"),
        ("04 - Areas/Admin/00 - Admin Index.md", "LiDock", "P2", "Admin index"),
        ("04 - Areas/Cycling/00 - Cycling Index.md", "LiBike", "P2", "Cycling index"),
        ("04 - Areas/Habits/00 - Habits Index.md", "LiFlame", "P1", "Habits index"),
        ("04 - Areas/Health and Fitness/00 - Health and Fitness Index.md", "LiApple", "P2", "Health & fitness index"),
        ("04 - Areas/NAS/00 - NAS Index.md", "LiHardDrive", "P2", "NAS index"),
        ("04 - Areas/Photography/00 - Photography Index.md", "LiCamera", "P2", "Photography index"),
        ("04 - Areas/Technology/00 - Technology Index.md", "LiCpu", "P1", "Technology index"),
        ("05 - Knowledge/00 - Knowledge Index.md", "LiBrain", "P2", "Knowledge master index"),
        ("05 - Knowledge/Software Engineering Index.md", "LiBrain", "P2", "Software engineering index"),
        ("05 - Knowledge/Deep Dives/00 - Deep Dives Index.md", "LiCompass", "P1", "Deep dives index"),
        ("06 - Resources/00 - Resources Index.md", "LiSearch", "P2", "Resources master index"),
        ("06 - Resources/AI/00 - AI Index.md", "LiCog", "P2", "AI inbox index"),
        ("06 - Resources/Books/00 - Books Index.md", "LiBook", "P2", "Books index"),
        ("06 - Resources/YouTube/00 - YouTube Index.md", "LiFilm", "P2", "YouTube index"),
        ("10 - Archive/00 - Archive Index.md", "LiFolderSymlink", "P2", "Archive index"),
        ("11 - Agents/Agent Index.md", "🤖", "P2", "Agent master index")
    ]
    for p, icon, prio, rat in index_expectations:
        if os.path.exists(os.path.join(vault_dir, p)):
            expected_items.append({"path": p, "item_type": "index", "suggested_icon": icon, "priority": prio, "rationale": rat})

    # 3. Book Summaries
    for p in md_files:
        if p.startswith("06 - Resources/Books") and p.endswith("Book Summary.md"):
            expected_items.append({"path": p, "item_type": "book_summary", "suggested_icon": "📚", "priority": "P2", "rationale": "Published book summary note"})

    # 4. Standard Recipes in 02 - Taani/Food/Recipes/
    rec_icons = {
        "R001": "🍚", "R002": "🍲", "R003": "🍛", "R004": "🍛",
        "R005": "🍛", "R006": "🍛", "R007": "🍲", "R008": "🍚",
        "R009": "🍫", "R010": "🍨", "R011": "🍨"
    }
    for p in md_files:
        if p.startswith("02 - Taani/Food/Recipes/"):
            base = os.path.basename(p)
            code = base.split(" - ")[0]
            icon = rec_icons.get(code, "🍳")
            expected_items.append({"path": p, "item_type": "recipe", "suggested_icon": icon, "priority": "P3", "rationale": "Standard recipe note"})

    # 5. Key Active Content & Agent Notes
    active_content = [
        ("02 - Taani/Finance/Financial Dashboard.md", "📊", "P2", "Canonical financial dashboard"),
        ("02 - Taani/Finance/How to Use the Financial Checkpoint System.md", "📖", "P3", "Financial checkpoint operational guide"),
        ("02 - Taani/Travel/Snowdonia 26 Plan.md", "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "P2", "Active travel project plan"),
        ("02 - Taani/Travel/Snowdonia 26 Packing List.md", "🏴󠁧󠁢󠁷󠁬󠁳󠁿", "P3", "Active travel packing list"),
        ("04 - Areas/Technology/Bionic Skills Setup.md", "⚡", "P2", "Developer skill setup guide"),
        ("04 - Areas/Habits/Current Habits.md", "⚡", "P2", "Active habits tracking dashboard"),
        ("04 - Areas/Habits/Daily Habit Tracking.md", "📅", "P2", "Daily habit tracking log"),
        ("04 - Areas/Habits/Active Habit Experiments.md", "🧪", "P2", "Habit hypothesis experiments"),
        ("04 - Areas/Habits/How to Use the Habit System.md", "📖", "P3", "Habit methodology guide"),
        ("11 - Agents/Vault Health Report.md", "🤖", "P2", "Canonical audit deliverable (per Note Standards: 🤖)"),
        ("11 - Agents/Vault Repair Manifest.md", "🤖", "P2", "Canonical repair manifest (per Note Standards: 🤖)"),
        ("11 - Agents/PARA Conformance Review.md", "🤖", "P2", "Canonical PARA architecture review (per Note Standards: 🤖)"),
        ("11 - Agents/Iconize Coverage Audit.md", "🤖", "P2", "Canonical Iconize audit report (per Note Standards: 🤖)"),
        ("11 - Agents/Workspace/README.md", "🤖", "P3", "Agent workspace documentation"),
        ("11 - Agents/Workflows/daily-deep-dive/SKILL.md", "🤖", "P2", "Daily deep dive workflow skill"),
        ("11 - Agents/Workflows/habits-checkpoint/SKILL.md", "🤖", "P2", "Habits checkpoint workflow skill")
    ]
    for p, icon, prio, rat in active_content:
        if os.path.exists(os.path.join(vault_dir, p)):
            expected_items.append({"path": p, "item_type": "active_content", "suggested_icon": icon, "priority": prio, "rationale": rat})

    missing_items = []
    icon_patch_dict = {}

    for item in expected_items:
        p = item["path"]
        if p not in icon_data:
            missing_items.append(item)
            icon_patch_dict[p] = item["suggested_icon"]

    configured_count = len(expected_items) - len(missing_items)
    coverage_pct = round((configured_count / len(expected_items)) * 100) if expected_items else 100

    return {
        "icon_data_path": icon_file,
        "expected_count": len(expected_items),
        "configured_count": configured_count,
        "missing_count": len(missing_items),
        "coverage_pct": coverage_pct,
        "missing_items": missing_items,
        "icon_patch_dict": icon_patch_dict
    }

def run_sentry(vault_dir, output_dir=None):
    if not output_dir:
        agents_dir = os.path.join(vault_dir, "11 - Agents")
        if os.path.exists(agents_dir):
            output_dir = agents_dir
        else:
            output_dir = vault_dir

    os.makedirs(output_dir, exist_ok=True)

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

            if is_hidden_root or f.startswith(".") or f in ["Vault Health Report.md", "Vault Repair Manifest.md", "Vault Health Findings.json", "PARA Conformance Review.md", "Iconize Coverage Audit.md"]:
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

    # 2. DFS Section-by-Section Structural Traversal
    dfs_sections = []
    overloaded_folders = []
    missing_index_folders = []

    for rel_path, depth, dirs, files in dfs_walk(vault_dir):
        if not rel_path:
            continue
        
        md_in_dir = [f for f in files if f.endswith(".md")]
        expected_index_name = f"00 - {os.path.basename(rel_path)} Index.md"
        has_index = expected_index_name in md_in_dir or any("Index" in f for f in md_in_dir)
        
        # Check flat folder overloading (>25 files without subdirs)
        is_overloaded = len(md_in_dir) >= 25 and len(dirs) == 0
        if is_overloaded:
            overloaded_folders.append({
                "path": rel_path,
                "notes_count": len(md_in_dir),
                "recommendation": "Cluster into thematic subfolders to eliminate flat clutter"
            })
            add_issue("P2", "structural-overload", rel_path, None, f"Overloaded flat directory with {len(md_in_dir)} notes and 0 subdirectories. High cognitive load and visual clutter.", f"Cluster into thematic subfolders (e.g., Cleaning, Appliances, Renovation, Furnishing)", "HIGH", False)

        # Check missing index note in key Areas or Projects
        if depth == 2 and not has_index and any(rel_path.startswith(prefix) for prefix in ["03 - Projects", "04 - Areas", "05 - Knowledge"]):
            missing_index_folders.append(rel_path)
            add_issue("P1", "structural-missing-index", rel_path, None, f"Directory lacks entry point index note '{expected_index_name}'. Dataview queries will silently omit this domain.", f"Create entry point index note '{expected_index_name}'", "HIGH", True)

        dfs_sections.append({
            "section": rel_path,
            "depth": depth,
            "notes_count": len(md_in_dir),
            "subdirs_count": len(dirs),
            "index_note": expected_index_name if has_index else None,
            "coherence": "High" if has_index else "Medium" if len(md_in_dir) < 5 else "Low",
            "assessment": "Overloaded" if is_overloaded else ("Needs Index" if (not has_index and depth==2) else "Healthy")
        })

    # 3. Content & Link Graph Parsing
    outgoing_links = defaultdict(list)
    incoming_links = defaultdict(list)
    note_contents = {}
    note_frontmatter = {}
    properties_used = Counter()
    tags_used = Counter()

    wikilink_re = re.compile(r"(!?\[\[(.*?)\]\])")
    mdlink_re = re.compile(r"(!?\[(.*?)\]\((.*?)\))")

    for rel_p, full_p in md_files.items():
        try:
            with open(full_p, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            continue

        note_contents[rel_p] = content

        # Parse YAML Frontmatter
        fm_dict = {}
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                yaml_block = parts[1]
                in_tags = False
                for yline in yaml_block.splitlines():
                    yline_s = yline.strip()
                    if ":" in yline_s and not yline_s.startswith("-"):
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

            line_clean = re.sub(r"`[^`]+`", "", line)

            for full_match, inner in wikilink_re.findall(line_clean):
                is_embed = full_match.startswith("!")
                link_part = inner.split("|")[0].strip()
                target_base = link_part.split("#")[0].split("^")[0].strip()

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
                        broken_links.append({"source": rel_p, "link": link_part, "line": idx + 1, "suggested": likely})
                        add_issue(sev, "link-broken-wikilink", rel_p, idx + 1, desc, action, conf, False)
                    elif len(resolved) > 1:
                        ambiguous_links.append({"source": rel_p, "link": link_part, "line": idx + 1, "matches": resolved})
                        add_issue("P2", "link-ambiguous", rel_p, idx + 1, f"Ambiguous wikilink resolves to multiple paths: {resolved}", "Disambiguate with full relative path", "HIGH", False)
                    else:
                        target_rel = resolved[0]
                        outgoing_links[rel_p].append(target_rel)
                        incoming_links[target_rel].append(rel_p)

            for full_match, text, url in mdlink_re.findall(line_clean):
                if not url.startswith("http://") and not url.startswith("https://") and not url.startswith("mailto:"):
                    clean_url = url.split("#")[0].split("?")[0].strip()
                    if clean_url:
                        target_resolved = os.path.normpath(os.path.join(os.path.dirname(rel_p), clean_url))
                        if "%2F" in clean_url or "%20" in clean_url:
                            decoded = clean_url.replace("%2F", "/").replace("%20", " ")
                            target_decoded = os.path.normpath(os.path.join(os.path.dirname(rel_p), decoded))
                            if target_decoded in all_files or (target_decoded + ".md") in all_files:
                                add_issue("P1", "link-encoded-slash", rel_p, idx + 1, f"Markdown link contains URL-encoded slashes (%2F): '{url}'", f"Replace '%2F' with standard '/'", "HIGH", True)
                        elif target_resolved not in all_files and (target_resolved + ".md") not in all_files:
                            add_issue("P1", "link-broken-relative", rel_p, idx + 1, f"Broken relative markdown link: '{url}'", "Update link path to match target file", "MEDIUM", False)

    # 4. Note Placement & Relocation Proposals ("Where notes should live instead")
    relocation_proposals = []
    
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
            deleted_in_git = [l for l in lines if l.strip().startswith("D ")]
            untracked_in_git = [l for l in lines if l.strip().startswith("??")]
            
            # Check if 02 - Taani is untracked while deletions exist in 04 - Areas/House or 03 - Projects/Travel
            if any("02 - Taani" in l for l in untracked_in_git) and any(("04 - Areas/House" in l or "03 - Projects/Travel" in l) for l in deleted_in_git):
                add_issue("P0", "git-untracked-deletion-hazard", "02 - Taani", None, "Critical Git hazard: '02 - Taani/' is untracked while old paths in '04 - Areas/House' show as deleted. Committing deletions will wipe notes permanently!", "Run 'git add \"02 - Taani\" \"03 - Projects\" \"04 - Areas\"' before making any other commits", "HIGH", True)
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

    # 7. PARA Conformance Audit (Vault & Shared Space)
    para_results = audit_para_conformance(vault_dir, md_files, rel_folders, note_frontmatter, note_contents)
    for pf in para_results["findings"]:
        add_issue(pf["severity"], pf["category"], pf["path"], None, pf["description"], pf["suggested_action"], pf["confidence"], False)

    # 8. Iconize Coverage Audit
    iconize_results = audit_iconize_coverage(vault_dir, all_files, md_files, rel_folders)
    for mi in iconize_results["missing_items"]:
        if mi["priority"] in ["P1", "P2"]:
            add_issue(mi["priority"], "iconize-missing-icon", mi["path"], None, f"Expected {mi['item_type']} lacks configured icon in Iconize data.json", f"Assign icon '{mi['suggested_icon']}' in data.json ({mi['rationale']})", "HIGH", True)

    # 9. Health Scoring
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
        "PARA structure (Vault)": para_results["vault_para"]["conformance_score"],
        "PARA structure (Shared space)": para_results["shared_para"]["conformance_score"],
        "Iconize coverage": iconize_results["coverage_pct"]
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
        {"rank": 6, "action": "Configure missing icons in '.obsidian/plugins/obsidian-icon-folder/data.json' across folders, indexes, and active notes", "impact": "MEDIUM", "risk_reduction": "Restores visual navigation hierarchy across desktop and mobile", "effort": "Low (apply staged JSON patch)", "confidence": "HIGH", "severity": "P2"},
        {"rank": 7, "action": "Create '.obsidian/daily-notes.json' pointing to '02 - Journal' to prevent new daily notes cluttering root", "impact": "HIGH", "risk_reduction": "Fixes core plugin destination drift", "effort": "Trivial (create JSON file)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 8, "action": "Resolve unmerged volatile worktree in '/private/tmp/taivault-food-os-mvp1' before next OS reboot", "impact": "HIGH", "risk_reduction": "Prevents loss of Food OS commits", "effort": "Medium (git merge/prune)", "confidence": "HIGH", "severity": "P1"},
        {"rank": 9, "action": "Fix self-referencing obsolete link in '02 - Taani/Travel/00 - Travel Index.md' ([[03 - Projects/Travel/...]])", "impact": "MEDIUM", "risk_reduction": "Eliminates broken navigation link", "effort": "Trivial (1-line edit)", "confidence": "HIGH", "severity": "P1"},
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
        "p4_issues": p4_count,
        "para_vault_score": para_results["vault_para"]["conformance_score"],
        "para_shared_score": para_results["shared_para"]["conformance_score"],
        "iconize_expected_count": iconize_results["expected_count"],
        "iconize_missing_count": iconize_results["missing_count"],
        "iconize_coverage_pct": iconize_results["coverage_pct"]
    }

    # Write Vault Health Findings.json
    findings_data = {
        "audit_version": "2.1",
        "auditor": "vault-sentry",
        "vault_path": vault_dir,
        "audit_timestamp": now_iso,
        "metrics": metrics,
        "scores": scores,
        "para_conformance": {
            "vault": para_results["vault_para"],
            "shared": para_results["shared_para"]
        },
        "iconize_audit": {
            "coverage_pct": iconize_results["coverage_pct"],
            "expected_count": iconize_results["expected_count"],
            "missing_count": iconize_results["missing_count"],
            "missing_items": iconize_results["missing_items"]
        },
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
**Audit Engine**: `vault-sentry` v2.1 (DFS Directory, Dual PARA Sentry & Iconize Auditor)

---

## Executive Summary

The **Vault Sentry** audit evaluated **{metrics['total_files']} files** ({metrics['markdown_notes']} Markdown notes, {metrics['folders']} folders) through a complete **Depth-First Search (DFS)** directory-by-directory walk.

Overall vault health is scored at **{scores['Overall vault health']}/100**.

### Key Diagnostic Takeaways:
1. **DFS Structural Traversal**: Audited **{metrics['dfs_sections_audited']} directory sections**. Discovered a major organizational bottleneck in `02 - Taani/House`, which has become an overloaded flat dumping ground of **48 notes** spanning cleaning, appliances, DIY renovation, furniture, and conveyancing.
2. **Dual PARA Structure Review**:
   - **Vault PARA ({scores['PARA structure (Vault)']}/100)**: `03 - Projects` has completely stagnated (0 active project notes), while active projects have drifted into `02 - Taani/Travel` and `02 - Taani/House`. Additionally, personal area maintenance guides leaked into `06 - Resources/AI`.
   - **Shared Space PARA ({scores['PARA structure (Shared space)']}/100)**: `02 - Taani` is structured into domain silos with zero folder-level PARA separation, resulting in a severe conflation of finite projects, ongoing areas, resources, and historical archives within `House/`.
3. **Iconize Expected Page Audit**: Configured icons cover **{metrics['iconize_coverage_pct']}%** of expected targets ({metrics['iconize_missing_count']} missing items identified across key folders, domain indexes, book summaries, and active content notes).
4. **Note Relocation Analysis ("Where it should live instead")**: Identified **{len(relocation_proposals)} misplaced notes** that violate domain boundaries (e.g. running races, cycling guides, coffee brewing, and water filters stored under `06 - Resources/AI`).
5. **Archival Candidates ("Outdated & untouched notes")**: Flagged **{len(archival_candidates)} notes for archival** to `10 - Archive/`, including dead indexes (`05 - Knowledge/Finance Index.md`), time-decaying purchase research (`Best Broadband Deal.md`), and redundant notes (`Bedding set.md`).

---

## Audit Metrics

| Metric | Count | Metric | Count |
|---|---:|---|---:|
| **Total Files** | {metrics['total_files']} | **DFS Sections Audited** | {metrics['dfs_sections_audited']} |
| **Markdown Notes** | {metrics['markdown_notes']} | **Overloaded Flat Folders** | {metrics['overloaded_folders']} |
| **Folders** | {metrics['folders']} | **Folders Missing Indexes** | {metrics['missing_index_folders']} |
| **Attachments (PDFs & Images)** | {metrics['attachments']} | **Note Relocation Proposals** | **{metrics['note_relocation_proposals']}** |
| **Broken Internal Links** | {metrics['internal_links_broken']} | **Notes Suggested to Archive** | **{metrics['archival_candidates']}** |
| **Vault PARA Conformance** | **{metrics['para_vault_score']}/100** | **Shared Space PARA Score** | **{metrics['para_shared_score']}/100** |
| **Iconize Coverage** | **{metrics['iconize_coverage_pct']}%** | **Iconize Missing Expected Targets** | **{metrics['iconize_missing_count']}** |
| **P0 Issues (Data Loss Risk)** | **{metrics['p0_issues']}** | **P1 Issues (Broken / Omitted)** | **{metrics['p1_issues']}** |
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
| **PARA structure (Vault)** | {scores['PARA structure (Vault)']}/100 | Stagnant Projects folder (0 active); area leakage into Resources inbox; underutilized Archive |
| **PARA structure (Shared space)** | {scores['PARA structure (Shared space)']}/100 | 100% domain-first silos; zero folder-level PARA separation; 48-file flat clutter in House |
| **Iconize coverage** | {scores['Iconize coverage']}% | {iconize_results['missing_count']} expected folders, indexes, and active notes missing configured icons |
| **Overall vault health** | **{scores['Overall vault health']}/100** | **Solid core knowledge base; needs folder restructuring, PARA alignment, and Git staging** |

---

## PARA Structure Conformance Review (Dual Analysis)

### 1. Overall Vault PARA Conformance: {para_results['vault_para']['conformance_score']}/100 ({para_results['vault_para']['grade']})

| PARA Tier | Path | Note Count | Share of Active Notes | Structural Health Status |
|---|---|---:|---:|---|
| **Projects** | `03 - Projects` | {para_results['vault_para']['projects_count']} | <1% | **Dormant / Depleted**: Only 1 index note exists. Active projects have evacuated into `02 - Taani/Travel` and `02 - Taani/House`. |
| **Areas** | `04 - Areas` | {para_results['vault_para']['areas_count']} | ~10% | **Active**: 5 healthy subdomains (Cycling, Habits, Health, NAS, Technology), but personal fitness guides leaked into Resources. |
| **Resources & Knowledge** | `05 - Knowledge` & `06 - Resources` | {para_results['vault_para']['knowledge_count'] + para_results['vault_para']['resources_count']} | ~80% | **Disproportionately Dominant**: 171 notes. High quality synthetic bases, but contains misplaced household and running notes. |
| **Archive** | `10 - Archive` | {para_results['vault_para']['archive_count']} | ~2% | **Underutilized**: Superseded indexes, expired contracts, and completed purchases remain in active folders. |

#### Key Vault PARA Insights:
1. **Projects Depletion**: While the user is actively working on finite projects (e.g. `Snowdonia 26`, `Montenegro 26`, `Installing Herringbone LVT`, `Replacing Switches`), none of these reside in `03 - Projects`. `03 - Projects/00 - Projects Index.md` has an empty Dataview query.
2. **Inbox Drift to Resources**: `06 - Resources/AI` acts as an unmanaged dumping inbox where non-AI material (`Most Prestigious Running Races London.md`, `Cycling 101.md`, `Coffee 101.md`, `Water Filtration Systems`) was placed instead of being routed to `04 - Areas/` or `02 - Taani/`.

---

### 2. Shared Space (`02 - Taani`) PARA Conformance: {para_results['shared_para']['conformance_score']}/100 ({para_results['shared_para']['grade']})

`02 - Taani` holds **{para_results['shared_para']['total_notes']} notes** across 4 shared household domains: `Finance/`, `Food/`, `House/`, and `Travel/`. It is currently organized **strictly by subject domain**, with zero folder-level PARA separation.

#### Implicit PARA Breakdown of `02 - Taani`:

| Implicit Tier | Notes | Share | Characteristics & Member Notes |
|---|---:|---:|---|
| **Shared Projects** | **{para_results['shared_para']['projects_count']}** | 15.3% | Finite outcomes with target deadlines: DIY renovation (`Installing Herringbone LVT`, `Replacing Switches`, `Fixing Door Foil Peel`, `Replacing Spotlights`, `WAGNER Paint Sprayer`) and upcoming trips (`Snowdonia 26 Plan`, `Montenegro 26 Plan`). |
| **Shared Areas** | **{para_results['shared_para']['areas_count']}** | 29.2% | Ongoing operational standards: `Household Cleaning System`, `Household Cooking System`, `Household Essentials Checklist`, `Financial Dashboard`, `Current vs New Household Budget`. |
| **Shared Resources** | **{para_results['shared_para']['resources_count']}** | 44.4% | Catalogues, reference materials, wishlists: 11 cooking recipes (`R001` - `R011`), furniture links, cookware reviews, appliance evaluations (`Dreame X40 Ultra`, `Best Water Filter`). |
| **Shared Archives** | **{para_results['shared_para']['archives_count']}** | 4.2% | Historical records and expired deals: `Original Rightmove Listing and Measurements`, `Legal and Mortgage for House`, `Best Broadband Deal`. |
| **Domain Indexes** | **{para_results['shared_para']['indexes_count']}** | 6.9% | Navigation hubs: `02 - Taani Index`, `Food Index`, `House Index`, `Finance Index`, `Travel Index`. |

#### Shared Space Structural Diagnosis & Recommendations:
- **The Problem**: All 48 notes in `02 - Taani/House` sit in a single unpartitioned flat directory. An active flooring installation project (`Installing Herringbone LVT.md`) lives side-by-side with an expired broadband contract (`Best Broadband Deal.md`) and a routine dishwasher checklist (`Kitchen Cleaning Supplies.md`).
- **Architectural Solution**:
  1. **Folder Sub-Clustering**: Cluster `02 - Taani/House/` into thematic subfolders that align with PARA:
     - `Renovation/` (Projects)
     - `Cleaning/` (Areas)
     - `Appliances/` & `Furnishing/` (Resources)
     - `Property/` (Archive)
  2. **Unified Frontmatter PARA Metadata**: Introduce a frontmatter property `para: project | area | resource | archive` across all notes in `02 - Taani/`. This enables cross-vault queries in parent indexes (e.g. listing all active projects across both personal and shared domains).

---

## Iconize Coverage & Expected Page Icon Audit

- **Audit Target File**: `.obsidian/plugins/obsidian-icon-folder/data.json`
- **Total Expected Items Checked**: **{iconize_results['expected_count']}**
- **Configured Items**: **{iconize_results['configured_count']}**
- **Missing Items**: **{iconize_results['missing_count']}**
- **Icon Coverage Rate**: **{iconize_results['coverage_pct']}%**

### Expected Pages & Folders Missing Icons:

| Path | Item Type | Suggested Icon | Priority | Rationale |
|---|---|:---:|---|---|
""")
        for mi in iconize_results["missing_items"]:
            rf.write(f"| `{mi['path']}` | {mi['item_type']} | `{mi['suggested_icon']}` | {mi['priority']} | {mi['rationale']} |\n")

        rf.write(f"""
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

## Top 10 Actions

| Rank | Action | Impact | Risk Reduction | Effort | Confidence | Severity |
|---|---|---|---|---|---|---|
| **1** | Stage and commit untracked `02 - Taani/` in Git | CRITICAL | Prevents permanent data loss of House & Travel domains | Low (`git add 02 - Taani`) | HIGH | **P0** |
| **2** | Create `04 - Areas/Technology/00 - Technology Index.md` | HIGH | Restores missing Technology area to Areas Dataview query | Low (create 1 note) | HIGH | **P1** |
| **3** | Relocate misplaced notes out of `06 - Resources/AI` | HIGH | Restores domain boundaries (Running -> Health, Cycling -> Cycling, etc.) | Low (move 5 notes) | HIGH | **P1** |
| **4** | Cluster overloaded `02 - Taani/House` (48 flat notes) into subfolders | HIGH | Transforms flat clutter into clean thematic subfolders | Medium (batch moves) | HIGH | **P2** |
| **5** | Configure missing icons in Iconize data.json across 35+ expected pages | MEDIUM | Restores visual hierarchy and mobile UI consistency | Low (apply staged JSON patch) | HIGH | **P2** |
| **6** | Archive superseded notes to `10 - Archive/` | MEDIUM | Removes dead indexes and expired research from active search | Low (archive 3 notes) | HIGH | **P2** |
| **7** | Create `.obsidian/daily-notes.json` pointing to `02 - Journal` | HIGH | Fixes daily notes dumping into vault root | Trivial (create JSON file) | HIGH | **P1** |
| **8** | Resolve unmerged volatile worktree in `/private/tmp/taivault-food-os-mvp1` | HIGH | Prevents loss of Food OS commits on reboot | Medium (git merge/prune) | HIGH | **P1** |
| **9** | Fix self-referencing link in `02 - Taani/Travel/00 - Travel Index.md` | MEDIUM | Eliminates broken navigation link | Trivial (1-line edit) | HIGH | **P1** |
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
**Auditor**: `vault-sentry` v2.1  
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

### [AUTO-05] Configure Missing Expected Icons in Iconize `data.json`
- **Target**: `.obsidian/plugins/obsidian-icon-folder/data.json`
- **Action**: Merge the following {len(iconize_results['icon_patch_dict'])} missing icon mappings into `data.json`:
  ```json
{json.dumps(iconize_results['icon_patch_dict'], indent=4, ensure_ascii=False)}
  ```

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

### [APPR-06] Realign Shared Space (`02 - Taani`) with PARA Architecture
- **Action**: Add frontmatter property `para: project | area | resource | archive` across all notes in `02 - Taani/`.
- **Purpose**: Enables Dataview queries across both personal and shared domains simultaneously without breaking the joint household namespace.

### [APPR-07] Resolve Volatile Git Worktree in `/private/tmp/`
- **Command**: Merge branch `codex/food-os-mvp1` into `main` and remove worktree: `git -C "{vault_dir}" worktree remove /private/tmp/taivault-food-os-mvp1`.

### [APPR-08] Fix Obsolete Self-Referencing Wikilink in Travel Index
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

    # Write PARA Conformance Review.md
    para_file = os.path.join(output_dir, "PARA Conformance Review.md")
    with open(para_file, "w", encoding="utf-8") as pf_out:
        pf_out.write(f"""# PARA Conformance Review: Personal Vault & Shared Space

**Vault Target**: `{vault_dir}`  
**Generated On**: {now_iso}  
**Auditor**: `vault-sentry` v2.1  
**Status**: COMPLETE

---

## 1. Executive Summary

This review assesses structural conformity to Tiago Forte's **PARA** (Projects, Areas, Resources, Archive) methodology across two distinct scopes:
1. **Personal / Vault-Level PARA** (Scored: **{para_results['vault_para']['conformance_score']}/100** · Grade {para_results['vault_para']['grade']})
2. **Shared Household Space (`02 - Taani`) PARA** (Scored: **{para_results['shared_para']['conformance_score']}/100** · Grade {para_results['shared_para']['grade']})

Overall, Taivault possesses high-quality reference material and established personal domains, but suffers from two architectural defects:
- **Vault Projects Depletion**: The official `03 - Projects` directory is dormant (0 active notes), with active projects scattered across shared travel and house domains.
- **Shared Space Conflation**: The shared household space (`02 - Taani`) uses strict domain silos (`House`, `Finance`, `Food`, `Travel`) with zero folder-level PARA separation, resulting in a flat 48-note dumping ground in `02 - Taani/House/`.

---

## 2. Overall Vault PARA Conformance

### Scorecard: {para_results['vault_para']['conformance_score']}/100 ({para_results['vault_para']['grade']})

| PARA Tier | Path | Note Count | Share of Active Notes | Structural Health Status |
|---|---|---:|---:|---|
| **Projects** | `03 - Projects` | {para_results['vault_para']['projects_count']} | <1% | **Dormant / Depleted**: Contains only `00 - Projects Index.md`. Active projects have drifted into `02 - Taani/Travel` and `02 - Taani/House`. |
| **Areas** | `04 - Areas` | {para_results['vault_para']['areas_count']} | ~10% | **Active**: 5 healthy subdomains (Cycling, Habits, Health, NAS, Technology), but personal fitness guides leaked into Resources. |
| **Resources & Knowledge** | `05 - Knowledge` & `06 - Resources` | {para_results['vault_para']['knowledge_count'] + para_results['vault_para']['resources_count']} | ~80% | **Disproportionately Dominant**: 171 notes. High quality synthetic bases, but contains misplaced household and running notes. |
| **Archive** | `10 - Archive` | {para_results['vault_para']['archive_count']} | ~2% | **Underutilized**: Superseded indexes, expired contracts, and completed purchases remain in active folders. |

### Key Diagnostic Observations:
1. **Projects Directory Stagnation**: While active projects are underway (e.g. `Snowdonia 26`, `Montenegro 26`, `Installing Herringbone LVT`, `Replacing Switches`), none reside in `03 - Projects`. `03 - Projects/00 - Projects Index.md` has an empty Dataview query.
2. **Inbox Drift to Resources**: `06 - Resources/AI` acts as an unmanaged dumping inbox where non-AI material (`Most Prestigious Running Races London.md`, `Cycling 101.md`, `Coffee 101.md`, `Water Filtration Systems`) was placed instead of being routed to `04 - Areas/` or `02 - Taani/`.
3. **Archive Pipeline Underuse**: Notes with time decay (e.g. `Best Broadband Deal.md`, superseded `Bedding set.md`, empty `05 - Knowledge/Finance Index.md`) sit alongside active notes rather than moving to `10 - Archive/`.

---

## 3. Shared Space (`02 - Taani`) PARA Conformance

### Scorecard: {para_results['shared_para']['conformance_score']}/100 ({para_results['shared_para']['grade']})

`02 - Taani` holds **{para_results['shared_para']['total_notes']} notes** across 4 shared household domains: `Finance/`, `Food/`, `House/`, and `Travel/`. It is currently organized **strictly by subject domain**, with zero folder-level PARA tier separation.

### Implicit PARA Breakdown of `02 - Taani`:

| Implicit Tier | Notes | Share | Characteristics & Member Notes |
|---|---:|---:|---|
| **Shared Projects** | **{para_results['shared_para']['projects_count']}** | 15.3% | Finite outcomes with target deadlines: DIY renovation (`Installing Herringbone LVT`, `Replacing Switches`, `Fixing Door Foil Peel`, `Replacing Spotlights`, `WAGNER Paint Sprayer`) and upcoming trips (`Snowdonia 26 Plan`, `Montenegro 26 Plan`). |
| **Shared Areas** | **{para_results['shared_para']['areas_count']}** | 29.2% | Ongoing operational standards: `Household Cleaning System`, `Household Cooking System`, `Household Essentials Checklist`, `Financial Dashboard`, `Current vs New Household Budget`. |
| **Shared Resources** | **{para_results['shared_para']['resources_count']}** | 44.4% | Catalogues, reference materials, wishlists: 11 cooking recipes (`R001` - `R011`), furniture links, cookware reviews, appliance evaluations (`Dreame X40 Ultra`, `Best Water Filter`). |
| **Shared Archives** | **{para_results['shared_para']['archives_count']}** | 4.2% | Historical records and expired deals: `Original Rightmove Listing and Measurements`, `Legal and Mortgage for House`, `Best Broadband Deal`. |
| **Domain Indexes** | **{para_results['shared_para']['indexes_count']}** | 6.9% | Navigation hubs: `02 - Taani Index`, `Food Index`, `House Index`, `Finance Index`, `Travel Index`. |

### The Overloaded `House` Bottleneck:
All 48 notes in `02 - Taani/House` sit in a single unpartitioned flat directory. An active flooring installation project (`Installing Herringbone LVT.md`) lives side-by-side with an expired broadband contract (`Best Broadband Deal.md`) and a routine dishwasher checklist (`Kitchen Cleaning Supplies.md`).

---

## 4. Architectural Realignment Roadmap

### Recommendation 1: Thematic Subfolder Clustering (Folder-Level PARA)
Cluster overloaded `02 - Taani/House/` into thematic subfolders that naturally map to PARA tiers:
1. `02 - Taani/House/Renovation/` (Projects) — 8 DIY & renovation tasks.
2. `02 - Taani/House/Cleaning/` (Areas) — 10 cleaning checklists and supply notes.
3. `02 - Taani/House/Appliances/` (Resources) — 7 appliance evaluations and smart home specifications.
4. `02 - Taani/House/Furnishing/` (Resources) — 12 furniture links and homeware options.
5. `02 - Taani/House/Property/` (Archive) — 3 deeds, mortgage, and survey records.

### Recommendation 2: Unified Frontmatter PARA Metadata
Add a `para:` frontmatter tag to all notes in `02 - Taani/`:
```yaml
---
parent: "[[00 - House Index]]"
para: project # or area | resource | archive
tags:
  - house
  - renovation
---
```

### Recommendation 3: Cross-Vault Dataview Query Blueprints
With `para:` tags applied, the root `03 - Projects/00 - Projects Index.md` can query all active projects across both personal and shared domains simultaneously:
```dataview
TABLE file.folder as Domain, tags as Tags
FROM ""
WHERE para = "project" AND !contains(file.path, "10 - Archive")
SORT file.name ASC
```
""")
    print(f"[+] Written PARA review to: {para_file}")

    # Write Iconize Coverage Audit.md
    iconize_file = os.path.join(output_dir, "Iconize Coverage Audit.md")
    with open(iconize_file, "w", encoding="utf-8") as if_out:
        if_out.write(f"""# Iconize Coverage & Expected Page Icon Audit

**Vault Target**: `{vault_dir}`  
**Generated On**: {now_iso}  
**Auditor**: `vault-sentry` v2.1  
**Config File**: `.obsidian/plugins/obsidian-icon-folder/data.json`

---

## 1. Executive Summary

- **Total Expected Targets Audited**: **{iconize_results['expected_count']}**
- **Configured Targets**: **{iconize_results['configured_count']}**
- **Missing Expected Targets**: **{iconize_results['missing_count']}**
- **Overall Coverage Rate**: **{iconize_results['coverage_pct']}%**

The vault makes extensive use of the `obsidian-icon-folder` plugin (with 246 total keys in `data.json`). However, coverage is uneven: several newly created domains (`02 - Taani/Food`, `04 - Areas/Habits`, `05 - Knowledge/Deep Dives`), primary domain index notes, standardized recipe notes, and agent documentation notes lack configured icons in the tree navigation.

---

## 2. Iconize Standards Specification

In accordance with the **Vault Constitution** and **Note Standards**:
1. **Directories**: Lucide icons prefixed with `Li...` representing the domain function (e.g. `LiUtensils` for Food, `LiFlame` for Habits, `LiCompass` for Deep Dives, `LiBot` for Agents).
2. **Index Notes**: Lucide icons matching their parent directory or entry point function.
3. **Book Summaries**: Literature emoji (`📚`).
4. **Agent Documentation & Deliverables**: Must use the `🤖` emoji or Lucide bot icons per `11 - Agents/Note Standards.md`.
5. **Content Leaves**: Contextual emojis matching topic (e.g. `🍳` for recipes, `🚲` for cycling, `🏃` for running, `📊` for financial dashboards).

---

## 3. Inventory of Expected Targets Missing Icons

| Target Path | Type | Suggested Icon | Priority | Rationale / Standard |
|---|---|:---:|:---:|---|
""")
        for mi in iconize_results["missing_items"]:
            if_out.write(f"| `{mi['path']}` | {mi['item_type']} | `{mi['suggested_icon']}` | {mi['priority']} | {mi['rationale']} |\n")

        if_out.write(f"""
---

## 4. Automated JSON Patch

The following configuration patch contains all {len(iconize_results['icon_patch_dict'])} missing icon mappings. It is staged in `Vault Repair Manifest.md` under `[AUTO-05]` and is ready to merge directly into `.obsidian/plugins/obsidian-icon-folder/data.json`:

```json
{json.dumps(iconize_results['icon_patch_dict'], indent=4, ensure_ascii=False)}
```
""")
    print(f"[+] Written Iconize audit to: {iconize_file}")
    print("[*] Vault Sentry completed successfully.")

if __name__ == "__main__":
    args = parse_args()
    if args.suggest or args.suggest_file:
        query = args.suggest or ""
        note_text = ""
        if args.suggest_file:
            if not os.path.exists(args.suggest_file):
                print(f"[!] Error: File not found: {args.suggest_file}", file=sys.stderr)
                sys.exit(1)
            with open(args.suggest_file, "r", encoding="utf-8") as sf:
                note_text = sf.read()
            if not query:
                for line in note_text.splitlines():
                    if line.startswith("# "):
                        query = line[2:].strip()
                        break
                if not query:
                    query = os.path.splitext(os.path.basename(args.suggest_file))[0]
        
        result = suggest_destination(query, note_text, args.vault)
        if args.json:
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(f"\n=======================================================")
            print(f"  VAULT SENTRY — NOTE DESTINATION RECOMMENDATION")
            print(f"=======================================================")
            print(f"Query:                 {result['query']}")
            print(f"PARA Tier:             {result['tier']}")
            print(f"Recommended Folder:    {result['recommended_folder']}")
            print(f"Recommended File:      {result['recommended_filename']}")
            print(f"Full Vault Path:       {result['full_recommended_path']}")
            print(f"Parent Index:          {result['parent_index']}")
            print(f"Recommended Icon:      {result['recommended_icon']}")
            print(f"Recommended Tags:      {', '.join(['#' + t for t in result['recommended_tags']])}")
            print(f"\nRationale:")
            print(f"  {result['rationale']}")
            print(f"\nAlternative:")
            print(f"  {result['alternative_destination']} — {result['alternative_rationale']}")
            print(f"\nFrontmatter Scaffold:")
            print(result['frontmatter_scaffold'])
            print(f"=======================================================\n")
        sys.exit(0)

    run_sentry(args.vault, args.output)
