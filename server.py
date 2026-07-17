import json
import os
import sqlite3
from pathlib import Path
from flask import Flask, jsonify, render_template, request, send_from_directory, abort

BASE_DIR = Path(__file__).parent
DB_PATH = BASE_DIR / 'progress.db'

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.executescript('''
        CREATE TABLE IF NOT EXISTS user_progress (
            username TEXT PRIMARY KEY,
            last_chapter INTEGER DEFAULT 0,
            last_card INTEGER DEFAULT 0,
            last_step INTEGER DEFAULT 0,
            viewing_quiz BOOLEAN DEFAULT 0,
            quiz_states TEXT,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        );
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
    conn.close()
    print("Database initialized.")

# Favicon
@app.route('/favicon.ico')
@app.route('/favicon.png')
def favicon():
    return send_from_directory(str(BASE_DIR), 'favicon.png', mimetype='image/png')

# Home — hardcoded like original index.html
@app.route('/')
def index():
    return render_template('index.html')

# Interactive lesson pages
@app.route('/course/<course_id>/lessons')
def course_lessons(course_id):
    conn = get_db()
    course = conn.execute("SELECT * FROM courses WHERE id=?", (course_id,)).fetchone()
    if not course:
        abort(404)
    course = dict(course)

    tutorials_raw = conn.execute("SELECT * FROM tutorials WHERE course_id=? ORDER BY sort_order", (course_id,)).fetchall()
    tutorials = []
    for t in tutorials_raw:
        t = dict(t)
        questions_raw = conn.execute(
            "SELECT l.* FROM lessons l WHERE l.tutorial_id=? ORDER BY l.sort_order", (t['id'],)
        ).fetchall()
        questions = []
        for q in questions_raw:
            q = dict(q)
            steps_raw = conn.execute(
                "SELECT title, body_html, diagram_mermaid FROM lesson_steps WHERE lesson_id=? ORDER BY sort_order",
                (q['id'],)
            ).fetchall()
            steps = []
            for s in steps_raw:
                s = dict(s)
                step = {'title': s['title'], 'body': s['body_html']}
                if s['diagram_mermaid']:
                    step['diagram'] = s['diagram_mermaid']
                steps.append(step)
            recaps_raw = conn.execute(
                "SELECT text FROM lesson_recaps WHERE lesson_id=? ORDER BY sort_order", (q['id'],)
            ).fetchall()
            recaps = [r['text'] for r in recaps_raw]
            questions.append({
                'number': q['number'],
                'title': q['title'],
                'intro': q['intro'],
                'steps': steps,
                'recap': recaps
            })
        tutorials.append({
            'id': t['id'],
            'title': t['title'],
            'short': t['short_title'],
            'questions': questions
        })

    glossary_raw = conn.execute("SELECT term, definition FROM glossary WHERE course_id=?", (course_id,)).fetchall()
    glossary = {r['term']: r['definition'] for r in glossary_raw}

    # secplus study page also needs quiz data (ALL_QUESTIONS)
    template = 'lesson.html'
    extra_vars = {}
    if course_id == 'secplus':
        template = 'study.html'
        quiz_raw = conn.execute(
            "SELECT * FROM quiz_questions WHERE course_id='secplus' ORDER BY sort_order", ()
        ).fetchall()
        quiz = [{'c': q['chapter_idx'], 'q': q['question_text'], 'o': json.loads(q['options_json']),
                 'a': q['correct_idx'], 'exp': dict(q).get('explanation', '') or ''} for q in quiz_raw]
        extra_vars['questions_json'] = json.dumps(quiz, ensure_ascii=False)

    conn.close()

    return render_template(template,
        course_id=course_id,
        course_name=course['name'],
        course_code=course.get('code', ''),
        course_icon=course.get('icon', '📖'),
        tutorials_json=json.dumps(tutorials, ensure_ascii=False),
        glossary_json=json.dumps(glossary, ensure_ascii=False),
        **extra_vars
    )

# Quiz pages
@app.route('/course/<course_id>/quiz')
def course_quiz(course_id):
    conn = get_db()
    course = conn.execute("SELECT * FROM courses WHERE id=?", (course_id,)).fetchone()
    if not course:
        abort(404)
    course = dict(course)

    questions_raw = conn.execute(
        "SELECT * FROM quiz_questions WHERE course_id=? ORDER BY sort_order", (course_id,)
    ).fetchall()
    chapters_raw = conn.execute(
        "SELECT name FROM quiz_chapters WHERE course_id=? ORDER BY chapter_idx", (course_id,)
    ).fetchall()

    chapters = [c['name'] for c in chapters_raw]
    if not chapters and questions_raw:
        max_c = max(q['chapter_idx'] for q in questions_raw)
        chapters = [f"Chapter {i+1}" for i in range(max_c + 1)]

    questions = []
    for qr in questions_raw:
        qr = dict(qr)
        questions.append({
            'c': qr['chapter_idx'],
            'q': qr['question_text'],
            'o': json.loads(qr['options_json']),
            'a': qr['correct_idx'],
            'e': qr.get('explanation', '') or ''
        })

    conn.close()

    template_map = {'ghf': 'quiz_ghf.html'}
    template = template_map.get(course_id, 'quiz.html')

    return render_template(template,
        course_name=course['name'],
        course_code=course.get('code', ''),
        course_icon=course.get('icon', '📖'),
        chapters_json=json.dumps(chapters, ensure_ascii=False),
        questions_json=json.dumps(questions, ensure_ascii=False)
    )

# Document pages
@app.route('/course/<course_id>/document')
def course_document(course_id):
    conn = get_db()
    course = conn.execute("SELECT * FROM courses WHERE id=?", (course_id,)).fetchone()
    if not course:
        abort(404)
    course = dict(course)

    sections = conn.execute(
        "SELECT content_html FROM document_sections WHERE course_id=? ORDER BY sort_order", (course_id,)
    ).fetchall()
    conn.close()

    content_html = '\n'.join(s['content_html'] for s in sections)
    return render_template('document.html',
        course_name=course['name'],
        content_html=content_html
    )

# API: Save progress
@app.route('/api/save', methods=['POST'])
def api_save():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'success': False, 'msg': 'Username required'}), 400
    conn = get_db()
    conn.execute('''
        INSERT OR REPLACE INTO user_progress
        (username, last_chapter, last_card, last_step, viewing_quiz, quiz_states, last_updated)
        VALUES (?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
    ''', (
        username,
        data.get('last_chapter', 0),
        data.get('last_card', 0),
        data.get('last_step', 0),
        1 if data.get('viewing_quiz') else 0,
        json.dumps(data.get('quiz_states', {}))
    ))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

# API: Load progress
@app.route('/api/load', methods=['POST'])
def api_load():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({'success': False, 'msg': 'Username required'}), 400
    conn = get_db()
    row = conn.execute(
        'SELECT last_chapter, last_card, last_step, viewing_quiz, quiz_states FROM user_progress WHERE username = ?',
        (username,)
    ).fetchone()
    conn.close()
    if row:
        resp = {
            'success': True,
            'last_chapter': row['last_chapter'],
            'last_card': row['last_card'],
            'last_step': row['last_step'],
            'viewing_quiz': bool(row['viewing_quiz']),
            'quiz_states': json.loads(row['quiz_states'] or '{}')
        }
    else:
        resp = {'success': False, 'msg': 'User not found'}
    return jsonify(resp)

# API: List users
@app.route('/api/users', methods=['POST'])
def api_users():
    conn = get_db()
    users = [r['username'] for r in conn.execute('SELECT username FROM user_progress').fetchall()]
    conn.close()
    return jsonify({'success': True, 'users': users})

# API: List courses
@app.route('/api/courses', methods=['GET', 'POST'])
def api_courses():
    conn = get_db()
    courses = conn.execute("SELECT id, code, name, icon, course_type FROM courses ORDER BY name").fetchall()
    conn.close()
    return jsonify({'success': True, 'courses': [dict(c) for c in courses]})

# Serve legacy static files (backward compat with old HTML files)
@app.route('/<path:filename>')
def serve_static(filename):
    filepath = BASE_DIR / filename
    if filepath.is_file() and not str(filepath).endswith('.py'):
        return send_from_directory(str(BASE_DIR), filename)
    abort(404)

if __name__ == '__main__':
    init_db()
    port = int(os.environ.get('PORT', 8000))
    print(f"Starting Flask server on port {port}... Open http://localhost:{port}/")
    app.run(host='0.0.0.0', port=port, debug=True)
