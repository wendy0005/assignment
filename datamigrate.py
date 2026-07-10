#!/usr/bin/env python3
"""One-time migration: extract HTML inline data → SQLite content tables."""

import sqlite3
import json
import re
import hashlib
import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'progress.db'

def extract_js_var(text, var_name):
    pattern = r'(?:const|let|var)\s+' + re.escape(var_name) + r'\s*=\s*'
    match = re.search(pattern, text)
    if not match:
        return None
    i = match.end()
    while i < len(text) and text[i] in ' \t\n\r':
        i += 1
    if i >= len(text):
        return None
    first_char = text[i]
    if first_char not in ('[', '{'):
        j = text.find(';', i)
        return text[i:j].strip() if j != -1 else text[i:].strip()
    close = ']' if first_char == '[' else '}'
    depth = 1
    in_single = in_double = in_backtick = False
    j = i + 1
    while j < len(text) and depth > 0:
        ch, prev = text[j], text[j-1] if j > 0 else ''
        if not in_single and not in_double and not in_backtick:
            if ch == "'": in_single = True
            elif ch == '"': in_double = True
            elif ch == '`': in_backtick = True
        else:
            if in_single and ch == "'" and prev != '\\': in_single = False
            elif in_double and ch == '"' and prev != '\\': in_double = False
            elif in_backtick and ch == '`' and prev != '\\': in_backtick = False
        if not in_single and not in_double and not in_backtick:
            if ch == first_char: depth += 1
            elif ch == close: depth -= 1
        if depth > 0: j += 1
    return text[i:j+1]


def convert_backtick_strings(text):
    result = []
    i = 0
    in_single = in_double = False
    while i < len(text):
        ch = text[i]
        if ch == '\\' and (in_single or in_double):
            result.append(ch)
            if i + 1 < len(text):
                result.append(text[i+1])
                i += 2
            continue
        if ch == "'" and not in_double:
            in_single = not in_single
            result.append(ch); i += 1; continue
        if ch == '"' and not in_single:
            in_double = not in_double
            result.append(ch); i += 1; continue
        if ch == '`' and not in_single and not in_double:
            j = i + 1
            while j < len(text) and text[j] != '`':
                j += 1
            if j < len(text):
                content = text[i+1:j]
                escaped = content.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
                result.append(f'"{escaped}"')
                i = j + 1
                continue
        result.append(ch)
        i += 1
    return ''.join(result)


def parse_js(js_text):
    import json5
    js_text = convert_backtick_strings(js_text)
    return json5.loads(js_text)


def fingerprint(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def init_content_tables(conn):
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS courses (
            id TEXT PRIMARY KEY,
            code TEXT,
            name TEXT NOT NULL,
            description TEXT,
            icon TEXT,
            course_type TEXT NOT NULL DEFAULT 'lesson',
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS tutorials (
            id TEXT PRIMARY KEY,
            course_id TEXT NOT NULL REFERENCES courses(id),
            title TEXT NOT NULL,
            short_title TEXT NOT NULL,
            c_idx INTEGER DEFAULT 0,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS lessons (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tutorial_id TEXT NOT NULL REFERENCES tutorials(id),
            number INTEGER NOT NULL,
            title TEXT NOT NULL,
            intro TEXT DEFAULT '',
            sort_order INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS lesson_steps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER NOT NULL REFERENCES lessons(id),
            title TEXT NOT NULL,
            body_html TEXT NOT NULL,
            diagram_mermaid TEXT,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS lesson_recaps (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lesson_id INTEGER NOT NULL REFERENCES lessons(id),
            text TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS glossary (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id TEXT NOT NULL REFERENCES courses(id),
            term TEXT NOT NULL,
            definition TEXT NOT NULL,
            UNIQUE(course_id, term)
        );
        CREATE TABLE IF NOT EXISTS quiz_questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id TEXT NOT NULL REFERENCES courses(id),
            chapter_idx INTEGER NOT NULL DEFAULT 0,
            question_text TEXT NOT NULL,
            options_json TEXT NOT NULL,
            correct_idx INTEGER NOT NULL,
            explanation TEXT DEFAULT '',
            card_ref INTEGER,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS quiz_chapters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id TEXT NOT NULL REFERENCES courses(id),
            chapter_idx INTEGER NOT NULL DEFAULT 0,
            name TEXT NOT NULL,
            UNIQUE(course_id, chapter_idx)
        );
        CREATE TABLE IF NOT EXISTS document_sections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            course_id TEXT NOT NULL REFERENCES courses(id),
            section_number TEXT,
            title TEXT NOT NULL,
            content_html TEXT NOT NULL,
            sort_order INTEGER NOT NULL DEFAULT 0
        );
    ''')
    conn.commit()


def migrate_iot_lessons(conn, filepath):
    print("  Migrating IoT Lessons...")
    text = filepath.read_text('utf-8')
    html_fp = fingerprint(text)

    glossary_js = extract_js_var(text, 'glossary')
    topics_js = extract_js_var(text, 'topics')
    if not topics_js:
        raise ValueError("Could not extract topics from iot_lessons.html")

    glossary = parse_js(glossary_js) if glossary_js else {}
    topics = parse_js(topics_js)

    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO courses (id, code, name, description, icon, course_type) VALUES (?,?,?,?,?,?)",
              ('iot', 'BCL1123', 'Internet of Things', 'IoT fundamentals: sensors, networks, protocols, and applications', '🌐', 'lesson'))

    for term, defn in glossary.items():
        c.execute("INSERT OR REPLACE INTO glossary (course_id, term, definition) VALUES (?,?,?)",
                  ('iot', term, defn))

    for ti, topic in enumerate(topics):
        tid = topic.get('id', f'topic{ti+1}')
        c.execute("INSERT OR REPLACE INTO tutorials (id, course_id, title, short_title, sort_order) VALUES (?,?,?,?,?)",
                  (tid, 'iot', topic['title'], topic.get('short', ''), ti))
        for qi, q in enumerate(topic.get('questions', [])):
            c.execute("INSERT INTO lessons (tutorial_id, number, title, intro, sort_order) VALUES (?,?,?,?,?)",
                      (tid, q['number'], q['title'], q.get('intro', ''), qi))
            lesson_id = c.lastrowid
            for si, step in enumerate(q.get('steps', [])):
                diagram = None
                body = step.get('body', '')
                # Some lessons embed mermaid inside body as <pre class="mermaid">
                c.execute("INSERT INTO lesson_steps (lesson_id, title, body_html, diagram_mermaid, sort_order) VALUES (?,?,?,?,?)",
                          (lesson_id, step['title'], body, diagram, si))
            for ri, recap in enumerate(q.get('recap', [])):
                c.execute("INSERT INTO lesson_recaps (lesson_id, text, sort_order) VALUES (?,?,?)",
                          (lesson_id, recap, ri))

    conn.commit()
    # Verify
    counts = {}
    counts['tutorials'] = c.execute("SELECT COUNT(*) FROM tutorials WHERE course_id='iot'").fetchone()[0]
    counts['lessons'] = c.execute("SELECT COUNT(*) FROM lessons l JOIN tutorials t ON l.tutorial_id=t.id WHERE t.course_id='iot'").fetchone()[0]
    counts['steps'] = c.execute("SELECT COUNT(*) FROM lesson_steps ls JOIN lessons l ON ls.lesson_id=l.id JOIN tutorials t ON l.tutorial_id=t.id WHERE t.course_id='iot'").fetchone()[0]
    counts['glossary'] = c.execute("SELECT COUNT(*) FROM glossary WHERE course_id='iot'").fetchone()[0]
    print(f"    → {counts}")
    return {'source_fingerprint': html_fp, 'counts': counts}


def migrate_database_lessons(conn, filepath):
    print("  Migrating Database Fundamentals Lessons...")
    text = filepath.read_text('utf-8')
    html_fp = fingerprint(text)

    glossary_js = extract_js_var(text, 'glossary')
    tutorials_js = extract_js_var(text, 'tutorials')
    if not tutorials_js:
        raise ValueError("Could not extract tutorials from database_interactive_lessons.html")

    glossary = parse_js(glossary_js) if glossary_js else {}
    tutorials = parse_js(tutorials_js)

    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO courses (id, code, name, description, icon, course_type) VALUES (?,?,?,?,?,?)",
              ('bcl1223', 'BCL1223', 'Database Fundamentals', 'Database concepts, relational models, SQL, and normalization', '🗄️', 'lesson'))

    for term, defn in glossary.items():
        c.execute("INSERT OR REPLACE INTO glossary (course_id, term, definition) VALUES (?,?,?)",
                  ('bcl1223', term, defn))

    for ti, tut in enumerate(tutorials):
        tid = tut.get('id', f'tutorial{ti+1}')
        c.execute("INSERT OR REPLACE INTO tutorials (id, course_id, title, short_title, sort_order, c_idx) VALUES (?,?,?,?,?,?)",
                  (tid, 'bcl1223', tut['title'], tut.get('short', ''), ti, tut.get('cIdx', ti)))
        for qi, q in enumerate(tut.get('questions', [])):
            c.execute("INSERT INTO lessons (tutorial_id, number, title, intro, sort_order) VALUES (?,?,?,?,?)",
                      (tid, q['number'], q['title'], q.get('intro', ''), qi))
            lesson_id = c.lastrowid
            for si, step in enumerate(q.get('steps', [])):
                diagram = step.get('diagram', None)
                body = step.get('body', '')
                c.execute("INSERT INTO lesson_steps (lesson_id, title, body_html, diagram_mermaid, sort_order) VALUES (?,?,?,?,?)",
                          (lesson_id, step['title'], body, diagram, si))
            for ri, recap in enumerate(q.get('recap', [])):
                c.execute("INSERT INTO lesson_recaps (lesson_id, text, sort_order) VALUES (?,?,?)",
                          (lesson_id, recap, ri))

    conn.commit()
    counts = {}
    counts['tutorials'] = c.execute("SELECT COUNT(*) FROM tutorials WHERE course_id='bcl1223'").fetchone()[0]
    counts['lessons'] = c.execute("SELECT COUNT(*) FROM lessons l JOIN tutorials t ON l.tutorial_id=t.id WHERE t.course_id='bcl1223'").fetchone()[0]
    counts['steps'] = c.execute("SELECT COUNT(*) FROM lesson_steps ls JOIN lessons l ON ls.lesson_id=l.id JOIN tutorials t ON l.tutorial_id=t.id WHERE t.course_id='bcl1223'").fetchone()[0]
    counts['glossary'] = c.execute("SELECT COUNT(*) FROM glossary WHERE course_id='bcl1223'").fetchone()[0]
    print(f"    → {counts}")
    return {'source_fingerprint': html_fp, 'counts': counts}


def migrate_secplus_study(conn, filepath):
    print("  Migrating Security+ Study (lessons + quiz)...")
    text = filepath.read_text('utf-8')
    html_fp = fingerprint(text)

    glossary_js = extract_js_var(text, 'glossary')
    tutorials_js = extract_js_var(text, 'tutorials')
    questions_js = extract_js_var(text, 'ALL_QUESTIONS')

    glossary = parse_js(glossary_js) if glossary_js else {}
    tutorials = parse_js(tutorials_js) if tutorials_js else []
    questions = parse_js(questions_js) if questions_js else []

    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO courses (id, code, name, description, icon, course_type) VALUES (?,?,?,?,?,?)",
              ('secplus', 'SY0-701', 'CompTIA Security+', 'Cybersecurity: threats, cryptography, networks, identity management, and compliance', '🔒', 'both'))

    for term, defn in glossary.items():
        c.execute("INSERT OR REPLACE INTO glossary (course_id, term, definition) VALUES (?,?,?)",
                  ('secplus', term, defn))

    for ti, tut in enumerate(tutorials):
        tid = tut.get('id', f'ch{ti}')
        c.execute("INSERT OR REPLACE INTO tutorials (id, course_id, title, short_title, sort_order, c_idx) VALUES (?,?,?,?,?,?)",
                  (tid, 'secplus', tut['title'], tut.get('short', ''), ti, tut.get('cIdx', ti)))
        for qi, q in enumerate(tut.get('questions', [])):
            c.execute("INSERT INTO lessons (tutorial_id, number, title, intro, sort_order) VALUES (?,?,?,?,?)",
                      (tid, q['number'], q['title'], q.get('intro', ''), qi))
            lesson_id = c.lastrowid
            for si, step in enumerate(q.get('steps', [])):
                diagram = step.get('diagram', None)
                body = step.get('body', '')
                c.execute("INSERT INTO lesson_steps (lesson_id, title, body_html, diagram_mermaid, sort_order) VALUES (?,?,?,?,?)",
                          (lesson_id, step['title'], body, diagram, si))
            for ri, recap in enumerate(q.get('recap', [])):
                c.execute("INSERT INTO lesson_recaps (lesson_id, text, sort_order) VALUES (?,?,?)",
                          (lesson_id, recap, ri))

    # Migrate quiz questions embedded in this file
    if questions:
        ch_names = list(dict.fromkeys(t['short'] for t in tutorials))
        for ci, name in enumerate(ch_names):
            c.execute("INSERT OR REPLACE INTO quiz_chapters (course_id, chapter_idx, name) VALUES (?,?,?)",
                      ('secplus', ci, name))
        for qi, q in enumerate(questions):
            explanation = q.get('exp', q.get('e', ''))
            card_ref = q.get('card', None)
            c.execute("INSERT INTO quiz_questions (course_id, chapter_idx, question_text, options_json, correct_idx, explanation, card_ref, sort_order) VALUES (?,?,?,?,?,?,?,?)",
                      ('secplus', q['c'], q['q'], json.dumps(q['o']), q['a'], explanation, card_ref, qi))

    conn.commit()
    counts = {}
    counts['tutorials'] = c.execute("SELECT COUNT(*) FROM tutorials WHERE course_id='secplus'").fetchone()[0]
    counts['lessons'] = c.execute("SELECT COUNT(*) FROM lessons l JOIN tutorials t ON l.tutorial_id=t.id WHERE t.course_id='secplus'").fetchone()[0]
    counts['quiz_qs'] = c.execute("SELECT COUNT(*) FROM quiz_questions WHERE course_id='secplus'").fetchone()[0]
    counts['glossary'] = c.execute("SELECT COUNT(*) FROM glossary WHERE course_id='secplus'").fetchone()[0]
    print(f"    → {counts}")
    return {'source_fingerprint': html_fp, 'counts': counts}


def migrate_quiz_generic(conn, filepath, course_id, code, name, desc, icon):
    """Generic migration for standalone quiz pages (security_plus_quiz, github_foundations_quiz)."""
    fname = filepath.name
    print(f"  Migrating {fname} → {course_id}...")
    text = filepath.read_text('utf-8')
    html_fp = fingerprint(text)

    questions_js = extract_js_var(text, 'ALL_QUESTIONS')
    domains_js = extract_js_var(text, 'DOMAINS') or extract_js_var(text, 'CH_NAMES')
    if not questions_js:
        raise ValueError(f"Could not extract ALL_QUESTIONS from {fname}")

    questions = parse_js(questions_js)
    domains = parse_js(domains_js) if domains_js else []

    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO courses (id, code, name, description, icon, course_type) VALUES (?,?,?,?,?,?)",
              (course_id, code, name, desc, icon, 'quiz'))

    for ci, ch_name in enumerate(domains):
        c.execute("INSERT OR REPLACE INTO quiz_chapters (course_id, chapter_idx, name) VALUES (?,?,?)",
                  (course_id, ci, ch_name))

    for qi, q in enumerate(questions):
        explanation = q.get('e', q.get('exp', ''))
        card_ref = q.get('card', None)
        c.execute("INSERT INTO quiz_questions (course_id, chapter_idx, question_text, options_json, correct_idx, explanation, card_ref, sort_order) VALUES (?,?,?,?,?,?,?,?)",
                  (course_id, q['c'], q['q'], json.dumps(q['o']), q['a'], explanation, card_ref, qi))

    conn.commit()
    counts = {}
    counts['chapters'] = c.execute("SELECT COUNT(*) FROM quiz_chapters WHERE course_id=?", (course_id,)).fetchone()[0]
    counts['questions'] = c.execute("SELECT COUNT(*) FROM quiz_questions WHERE course_id=?", (course_id,)).fetchone()[0]
    print(f"    → {counts}")
    return {'source_fingerprint': html_fp, 'counts': counts}


def migrate_document(conn, filepath, course_id, code, name, icon):
    """Migrate a static answer document."""
    fname = filepath.name
    print(f"  Migrating document {fname} → {course_id}...")
    text = filepath.read_text('utf-8')
    html_fp = fingerprint(text)

    # Extract body content between <body> and </body>
    body_match = re.search(r'<body[^>]*>(.*?)</body>', text, re.DOTALL)
    if not body_match:
        raise ValueError(f"Could not extract body from {fname}")
    body_html = body_match.group(1)

    # Extract title from <h1> or <title>
    title_match = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.DOTALL)
    title = title_match.group(1).strip() if title_match else name

    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO courses (id, code, name, description, icon, course_type) VALUES (?,?,?,?,?,?)",
              (course_id, code, name, '', icon, 'document'))

    c.execute("INSERT INTO document_sections (course_id, section_number, title, content_html, sort_order) VALUES (?,?,?,?,?)",
              (course_id, '1', title, body_html, 0))
    conn.commit()
    counts = {}
    counts['sections'] = 1
    print(f"    → {counts}")
    return {'source_fingerprint': html_fp, 'counts': counts}


def verify_migration(conn, results):
    print("\n=== VERIFICATION ===\n")
    all_ok = True
    for source_name, result in results.items():
        counts = result['counts']
        total = sum(counts.values())
        print(f"  {source_name}: {counts} (total {total})")
    print()
    # Count totals across all tables
    c = conn.cursor()
    tables = ['courses', 'tutorials', 'lessons', 'lesson_steps', 'lesson_recaps',
              'glossary', 'quiz_questions', 'quiz_chapters', 'document_sections']
    grand = 0
    for tbl in tables:
        cnt = c.execute(f"SELECT COUNT(*) FROM {tbl}").fetchone()[0]
        print(f"  {tbl}: {cnt} rows")
        grand += cnt
    print(f"\n  TOTAL ROWS: {grand}")
    print("  VERIFICATION COMPLETE")
    return all_ok


def main():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA journal_mode=WAL")

    print("=== DROP & RECREATE CONTENT TABLES ===")
    c = conn.cursor()
    c.executescript('''
        DROP TABLE IF EXISTS document_sections;
        DROP TABLE IF EXISTS quiz_questions;
        DROP TABLE IF EXISTS quiz_chapters;
        DROP TABLE IF EXISTS lesson_recaps;
        DROP TABLE IF EXISTS lesson_steps;
        DROP TABLE IF EXISTS lessons;
        DROP TABLE IF EXISTS glossary;
        DROP TABLE IF EXISTS tutorials;
        DROP TABLE IF EXISTS courses;
    ''')
    conn.commit()
    init_content_tables(conn)
    print("Content tables created.\n")

    results = {}

    results['iot_lessons'] = migrate_iot_lessons(
        conn, BASE_DIR / 'current_sem' / 'iot_lessons.html')

    results['database_lessons'] = migrate_database_lessons(
        conn, BASE_DIR / 'current_sem' / 'BCL1223 - Database Fundamentals' / 'database_interactive_lessons.html')

    results['secplus_study'] = migrate_secplus_study(
        conn, BASE_DIR / 'current_sem' / 'security_plus_study.html')

    results['secplus_quiz'] = migrate_quiz_generic(
        conn, BASE_DIR / 'current_sem' / 'security_plus_quiz.html',
        'secplus-quiz', 'SY0-701', 'CompTIA Security+ Quiz',
        'Practice quiz covering all 16 Security+ domains', '🔒')

    results['ghf_quiz'] = migrate_quiz_generic(
        conn, BASE_DIR / 'current_sem' / 'github_foundations_quiz.html',
        'ghf', 'GHF', 'GitHub Foundations',
        'Practice quiz for GitHub Foundations certification — 7 domains', '🐙')

    # Document pages
    doc_sources = [
        ('bcl1223-t1', 'BCL1223', 'Tutorial 1 — Database Concepts Answers',
         BASE_DIR / 'current_sem' / 'BCL1223 - Database Fundamentals' / 'Tutorial1_DatabaseConcepts_Answers.html', '📄'),
        ('bcl1223-t2', 'BCL1223', 'Tutorial 2 — Relational Data Models Answers',
         BASE_DIR / 'current_sem' / 'BCL1223 - Database Fundamentals' / 'Tutorial2_RelationalDataModels_Answers.html', '📄'),
        ('bcl1223-t3', 'BCL1223', 'Tutorial 3 Answers',
         BASE_DIR / 'current_sem' / 'BCL1223 - Database Fundamentals' / '20260710_Tutorial3_Answers.html', '📄'),
        ('bcl1223-test', 'BCL1223', 'Database Fundamentals Test Answers',
         BASE_DIR / 'current_sem' / 'BCL1223 - Database Fundamentals' / '20260710_Database_Fundamentals_Test_Answers.html', '📄'),
        ('bcl1233-a1', 'BCL1233', 'Assignment 1 — System Analysis',
         BASE_DIR / 'current_sem' / 'BCL1233 - System Analysis' / 'BCL1233Assignment1_Answers.html', '📄'),
        ('bcl1233-a2', 'BCL1233', 'Assignment 2 — System Analysis',
         BASE_DIR / 'current_sem' / 'BCL1233 - System Analysis' / 'BCL1233Assignment2_Answers.html', '📄'),
        ('bcl1233-a3', 'BCL1233', 'Assignment 3 — System Analysis',
         BASE_DIR / 'current_sem' / 'BCL1233 - System Analysis' / 'BCL1233Assignment3_Answers.html', '📄'),
    ]
    for cid, code, name, path, icon in doc_sources:
        if path.exists():
            results[f'doc_{cid}'] = migrate_document(conn, path, cid, code, name, icon)
        else:
            print(f"  SKIP: {path.name} not found")

    print()
    verify_migration(conn, results)
    conn.close()
    print("\nMigration complete. Content lives in progress.db")


if __name__ == '__main__':
    main()
