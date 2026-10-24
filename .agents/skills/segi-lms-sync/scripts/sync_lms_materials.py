#!/usr/bin/env python3
"""
SEGi Camu LMS Material Sync Script
Downloads course learning materials without re-downloading or overlapping with existing files.
Tracks downloads in a persistent manifest and checks file existence across directories.
"""

import os
import sys
import json
import time
import argparse
import requests
from datetime import datetime

MANIFEST_FILENAME = ".lms_manifest.json"

CATEGORIES = {
    "tutorial": "Tutorials",
    "lab": "Tutorials",
    "practice": "Tutorials",
    "document": "Course Documents",
    "pro-forma": "Course Documents",
    "introduction": "Course Documents",
    "overview": "Course Documents",
    "instruction": "Course Documents",
    "welcome": "Course Documents",
    "profile": "Course Documents",
    "book": "E-Books",
    "e-book": "E-Books",
    "reading": "E-Books",
    "lecture": "Lectures",
    "sim": "Lectures",
    "topic": "Lectures",
    "slide": "Lectures",
    "chapter": "Lectures"
}

def resolve_category(item):
    cat = (item.get("category") or "").lower()
    title = (item.get("title") or "").lower()
    chapter = (item.get("chapter") or "").lower()
    subchapter = (item.get("subchapter") or "").lower()
    text = f"{cat} {title} {chapter} {subchapter}"

    for kw, target_cat in CATEGORIES.items():
        if kw in text:
            return target_cat
    return "Lectures"

def load_manifest(manifest_path):
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[WARN] Could not read manifest ({e}), initializing empty manifest.")
    return {"version": 1, "items": {}}

def save_manifest(manifest_path, manifest_data):
    try:
        with open(manifest_path, "w", encoding="utf-8") as f:
            json.dump(manifest_data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[ERROR] Failed to save manifest: {e}")

def file_exists_in_course(course_path, filename):
    """Checks if the file already exists anywhere within the course directory."""
    for root, _, files in os.walk(course_path):
        if filename in files:
            full_path = os.path.join(root, filename)
            if os.path.getsize(full_path) > 0:
                return full_path
    return None

def sync_materials(input_json, target_dir, dry_run=False, force=False):
    if not os.path.exists(input_json):
        print(f"[ERROR] Input JSON not found at: {input_json}")
        sys.exit(1)

    with open(input_json, "r", encoding="utf-8") as f:
        courses = json.load(f)

    os.makedirs(target_dir, exist_ok=True)
    manifest_path = os.path.join(target_dir, MANIFEST_FILENAME)
    manifest = load_manifest(manifest_path)

    headers = {
        "Referer": "https://staff-spark.segi.edu.my/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }

    stats = {"skipped": 0, "downloaded": 0, "failed": 0, "total": 0}

    for course in courses:
        code = course.get("code", "UNKNOWN")
        name = course.get("name", "Course")
        course_folder_name = f"{code} - {name}"
        course_path = os.path.join(target_dir, course_folder_name)
        os.makedirs(course_path, exist_ok=True)

        files = course.get("files", [])
        print(f"\n=======================================================")
        print(f"Course: {course_folder_name} ({len(files)} items listed)")
        print(f"=======================================================")

        for item in files:
            stats["total"] += 1
            filename = item.get("fileName")
            url = item.get("url")
            item_id = item.get("id", filename)

            if not filename or not url:
                print(f"[SKIP] Invalid entry: {item}")
                continue

            category = resolve_category(item)
            dest_dir = os.path.join(course_path, category)
            dest_path = os.path.join(dest_dir, filename)

            # Check 1: De-duplication check against existing file in course
            existing_loc = file_exists_in_course(course_path, filename)
            
            # Check 2: Manifest record check. A record alone does not prove
            # that the file is still on disk; files can be moved or deleted.
            in_manifest = item_id in manifest.get("items", {})

            if not force and existing_loc:
                sz = os.path.getsize(existing_loc)
                print(f"  [ALREADY DOWNLOADED] {category}/{filename} ({sz:,} bytes) -> Skipped")
                stats["skipped"] += 1
                
                # Update manifest if missing
                if not in_manifest:
                    manifest["items"][item_id] = {
                        "filename": filename,
                        "course": course_folder_name,
                        "category": category,
                        "size_bytes": sz,
                        "path": os.path.relpath(existing_loc, target_dir),
                        "synced_at": datetime.now().isoformat()
                    }
                continue

            if not force and in_manifest and not existing_loc:
                print(f"  [STALE MANIFEST] {category}/{filename} is missing from disk; downloading again")
                manifest["items"].pop(item_id, None)

            if dry_run:
                print(f"  [WOULD DOWNLOAD] {category}/{filename} from {url}")
                stats["downloaded"] += 1
                continue

            # Perform download
            os.makedirs(dest_dir, exist_ok=True)
            temp_path = dest_path + ".tmp"
            print(f"  [DOWNLOADING] {category}/{filename} ...", end=" ", flush=True)

            try:
                with requests.get(url, headers=headers, stream=True, timeout=90) as res:
                    if res.status_code == 200:
                        with open(temp_path, "wb") as f_out:
                            for chunk in res.iter_content(chunk_size=1024 * 1024):
                                if chunk:
                                    f_out.write(chunk)
                        
                        # Atomic rename once verified
                        os.replace(temp_path, dest_path)
                        final_size = os.path.getsize(dest_path)
                        print(f"OK ({final_size:,} bytes)")
                        stats["downloaded"] += 1

                        # Record in manifest
                        manifest["items"][item_id] = {
                            "filename": filename,
                            "course": course_folder_name,
                            "category": category,
                            "size_bytes": final_size,
                            "path": os.path.relpath(dest_path, target_dir),
                            "url": url,
                            "synced_at": datetime.now().isoformat()
                        }
                        save_manifest(manifest_path, manifest)
                    else:
                        print(f"FAILED (HTTP {res.status_code})")
                        stats["failed"] += 1
            except Exception as e:
                print(f"ERROR: {e}")
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except:
                        pass
                stats["failed"] += 1

    save_manifest(manifest_path, manifest)
    print("\n-------------------------------------------------------")
    print(f"Sync Complete: {stats['downloaded']} downloaded, {stats['skipped']} skipped (no overlap), {stats['failed']} failed (Total: {stats['total']})")
    print(f"Manifest updated at: {manifest_path}")
    print("-------------------------------------------------------")

def main():
    parser = argparse.ArgumentParser(description="SEGi Camu LMS Material Sync with De-duplication")
    parser.add_argument("--input", default="/Users/jingyichan/CodingArea/assignment/lms_materials_all.json", help="Path to extracted LMS materials JSON")
    parser.add_argument("--target-dir", default="/Users/jingyichan/CodingArea/assignment/current_sem", help="Target root directory (current_sem)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate sync without downloading")
    parser.add_argument("--force", action="store_true", help="Force re-download of existing files")

    args = parser.parse_args()
    sync_materials(args.input, args.target_dir, dry_run=args.dry_run, force=args.force)

if __name__ == "__main__":
    main()
