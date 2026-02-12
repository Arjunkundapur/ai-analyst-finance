#!/usr/bin/env python3
"""
Rival — Early Access Server
Serves static files and handles waitlist form submissions.
"""

import json
import os
import http.server
import socketserver
from datetime import datetime

PORT = 8000
SUBMISSIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "submissions.json")


def load_submissions():
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, "r") as f:
            return json.load(f)
    return []


def save_submissions(submissions):
    with open(SUBMISSIONS_FILE, "w") as f:
        json.dump(submissions, f, indent=2)


class RivalHandler(http.server.SimpleHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/api/submit":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")

            try:
                data = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
                return

            data["submitted_at"] = datetime.now().isoformat()
            data["id"] = datetime.now().strftime("%Y%m%d%H%M%S%f")

            submissions = load_submissions()
            submissions.append(data)
            save_submissions(submissions)

            print(f"✅ New signup: {data.get('name', 'Unknown')} @ {data.get('firm', '?')} — Total: {len(submissions)}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "You're on the list! We'll reach out soon.",
                "total_submissions": len(submissions)
            }).encode())
        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def log_message(self, format, *args):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    with socketserver.TCPServer(("", PORT), RivalHandler) as httpd:
        print(f"""
╔══════════════════════════════════════════════╗
║   ⚡ Rival — Early Access Server             ║
║──────────────────────────────────────────────║
║   Running on: http://localhost:{PORT}          ║
║   Submissions saved to: submissions.json     ║
║   Press Ctrl+C to stop                       ║
╚══════════════════════════════════════════════╝
        """)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
