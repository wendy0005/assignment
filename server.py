import http.server
import json
import sqlite3
import os

def init_db():
    conn = sqlite3.connect('progress.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_progress (
            username TEXT PRIMARY KEY,
            last_chapter INTEGER DEFAULT 0,
            last_card INTEGER DEFAULT 0,
            last_step INTEGER DEFAULT 0,
            viewing_quiz BOOLEAN DEFAULT 0,
            quiz_states TEXT,
            last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()
    print("SQLite database initialized successfully.")

class ProgressHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        # Enable CORS for local development
        
        if self.path == '/api/save':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
            except Exception as e:
                self.send_error(400, "Invalid JSON")
                return
                
            username = data.get('username')
            if not username:
                self.send_error(400, "Username required")
                return
                
            conn = sqlite3.connect('progress.db')
            cursor = conn.cursor()
            cursor.execute('''
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
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}).encode('utf-8'))
            
        elif self.path == '/api/load':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            try:
                data = json.loads(post_data.decode('utf-8'))
            except Exception as e:
                self.send_error(400, "Invalid JSON")
                return
                
            username = data.get('username')
            if not username:
                self.send_error(400, "Username required")
                return
                
            conn = sqlite3.connect('progress.db')
            cursor = conn.cursor()
            cursor.execute('SELECT last_chapter, last_card, last_step, viewing_quiz, quiz_states FROM user_progress WHERE username = ?', (username,))
            row = cursor.fetchone()
            conn.close()
            
            if row:
                resp = {
                    "success": True,
                    "last_chapter": row[0],
                    "last_card": row[1],
                    "last_step": row[2],
                    "viewing_quiz": bool(row[3]),
                    "quiz_states": json.loads(row[4] or '{}')
                }
            else:
                resp = {"success": False, "msg": "User not found"}
                
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(resp).encode('utf-8'))

        elif self.path == '/api/users':
            conn = sqlite3.connect('progress.db')
            cursor = conn.cursor()
            cursor.execute('SELECT username FROM user_progress')
            users = [r[0] for r in cursor.fetchall()]
            conn.close()
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "users": users}).encode('utf-8'))
            
        else:
            self.send_error(404, "API not found")

    def do_OPTIONS(self):
        # Support CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

def run(port=8000):
    init_db()
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, ProgressHandler)
    print(f"Starting server on port {port}... Open http://localhost:{port}/")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        httpd.server_close()

if __name__ == '__main__':
    run()
