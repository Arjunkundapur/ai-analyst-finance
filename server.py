#!/usr/bin/env python3
"""
Car Showroom Enquiry Server
Serves static files and handles form submissions, saving them to a local JSON file.
"""

import json
import os
import http.server
import socketserver
from datetime import datetime
from urllib.parse import parse_qs

PORT = 8000
SUBMISSIONS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "submissions.json")


def load_submissions():
    """Load existing submissions from the JSON file."""
    if os.path.exists(SUBMISSIONS_FILE):
        with open(SUBMISSIONS_FILE, "r") as f:
            return json.load(f)
    return []


def save_submissions(submissions):
    """Save submissions to the JSON file."""
    with open(SUBMISSIONS_FILE, "w") as f:
        json.dump(submissions, f, indent=2)


class ShowroomHandler(http.server.SimpleHTTPRequestHandler):
    """Custom handler that serves static files and handles form POST requests."""

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

            # Add metadata
            data["submitted_at"] = datetime.now().isoformat()
            data["id"] = datetime.now().strftime("%Y%m%d%H%M%S%f")

            # Load existing submissions and append
            submissions = load_submissions()
            submissions.append(data)
            save_submissions(submissions)

            print(f"✅ New enquiry from {data.get('name', 'Unknown')} — Total: {len(submissions)}")

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "success": True,
                "message": "Thank you for your interest! We will contact you shortly.",
                "total_submissions": len(submissions)
            }).encode())

        elif self.path == "/api/submissions":
            submissions = load_submissions()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(submissions, indent=2).encode())

        else:
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Not found"}).encode())

    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def main():
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    with socketserver.TCPServer(("", PORT), ShowroomHandler) as httpd:
        print(f"""
╔══════════════════════════════════════════════╗
║   🚗  Car Showroom Enquiry Server  🚗       ║
║──────────────────────────────────────────────║
║   Running on: http://localhost:{PORT}          ║
║   Submissions saved to: submissions.json     ║
║   Press Ctrl+C to stop                       ║
╚══════════════════════════════════════════════╝
        """)
        httpd.serve_forever()


if __name__ == "__main__":
    main()
