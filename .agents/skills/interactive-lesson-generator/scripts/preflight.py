#!/usr/bin/env python3
"""Preflight overlap checker for interactive-lesson-generator.

Run this before writing a new migration script. It scans progress.db for
courses, tutorials, lessons, or glossary terms that may overlap with the
proposed new content. If anything looks related, ask the user how to proceed.
"""

import argparse
import sqlite3
import sys
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[4]
DB_PATH = BASE_DIR / "progress.db"


def keywords_from_args(args) -> list[str]:
    items = []
    for raw in (args.keyword or []):
        for part in raw.split(","):
            part = part.strip()
            if part:
                items.append(part.lower())
    return items


def search_db(conn, keywords: list[str]):
    c = conn.cursor()
    matches = {
        "courses": [],
        "tutorials": [],
        "lessons": [],
        "glossary": [],
    }

    for kw in keywords:
        like = f"%{kw}%"
        matches["courses"].extend(
            c.execute(
                "SELECT id, code, name, description FROM courses WHERE LOWER(id) LIKE ? OR LOWER(code) LIKE ? OR LOWER(name) LIKE ? OR LOWER(description) LIKE ?",
                (like, like, like, like),
            ).fetchall()
        )
        matches["tutorials"].extend(
            c.execute(
                "SELECT c.id, c.name, t.id, t.title, t.short_title FROM tutorials t JOIN courses c ON t.course_id = c.id WHERE LOWER(t.title) LIKE ? OR LOWER(t.short_title) LIKE ?",
                (like, like),
            ).fetchall()
        )
        matches["lessons"].extend(
            c.execute(
                "SELECT c.id, c.name, t.short_title, l.number, l.title FROM lessons l JOIN tutorials t ON l.tutorial_id = t.id JOIN courses c ON t.course_id = c.id WHERE LOWER(l.title) LIKE ? OR LOWER(l.intro) LIKE ?",
                (like, like),
            ).fetchall()
        )
        matches["glossary"].extend(
            c.execute(
                "SELECT c.id, c.name, g.term FROM glossary g JOIN courses c ON g.course_id = c.id WHERE LOWER(g.term) LIKE ? OR LOWER(g.definition) LIKE ?",
                (like, like),
            ).fetchall()
        )

    # Deduplicate by row content
    for key in matches:
        seen = set()
        deduped = []
        for row in matches[key]:
            signature = tuple(row)
            if signature not in seen:
                seen.add(signature)
                deduped.append(row)
        matches[key] = deduped

    return matches


def print_report(matches):
    total = sum(len(v) for v in matches.values())
    print(f"\nFound {total} potential overlap(s):\n")

    if matches["courses"]:
        print("🎓 Courses")
        for row in matches["courses"]:
            cid, code, name, desc = row
            print(f"   [{cid}] {code} — {name}")
            if desc:
                print(f"      {desc}")
        print()

    if matches["tutorials"]:
        print("📁 Tutorials / tabs")
        for row in matches["tutorials"]:
            cid, cname, tid, title, short = row
            print(f"   [{cid}] {cname} → {title} (short: {short})")
        print()

    if matches["lessons"]:
        print("📄 Lessons")
        for row in matches["lessons"]:
            cid, cname, tab, num, title = row
            print(f"   [{cid}] {cname} / {tab} / L{num}: {title}")
        print()

    if matches["glossary"]:
        print("📖 Glossary terms")
        for row in matches["glossary"]:
            cid, cname, term = row
            print(f"   [{cid}] {cname} → {term}")
        print()

    if total == 0:
        print("   No overlap detected. Safe to create a new course.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check progress.db for overlapping content before adding a new course."
    )
    parser.add_argument(
        "keyword",
        nargs="*",
        help="One or more keywords to search for. Comma-separated also works.",
    )
    parser.add_argument(
        "--proposed-id",
        help="Proposed course ID to check for exact duplicates.",
    )
    parser.add_argument(
        "--proposed-name",
        help="Proposed course name to check for similar names.",
    )
    parser.add_argument(
        "--db",
        type=Path,
        default=DB_PATH,
        help=f"Path to SQLite database. Default: {DB_PATH}",
    )
    parser.add_argument(
        "--exit-code",
        action="store_true",
        help="Exit with non-zero status if any overlap is found.",
    )

    args = parser.parse_args(argv)

    keywords = keywords_from_args(args)
    if args.proposed_id:
        keywords.append(args.proposed_id.lower())
    if args.proposed_name:
        keywords.append(args.proposed_name.lower())

    if not keywords:
        print("Error: supply at least one keyword, --proposed-id, or --proposed-name.")
        parser.print_help()
        return 1

    if not args.db.exists():
        print(f"Database not found at {args.db}. Nothing to overlap with yet.")
        return 0

    conn = sqlite3.connect(str(args.db))
    try:
        matches = search_db(conn, keywords)
        print_report(matches)

        if args.exit_code and any(matches.values()):
            return 2
        return 0
    finally:
        conn.close()


if __name__ == "__main__":
    sys.exit(main())
