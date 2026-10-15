
import os
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

import db

# The web folder contains our HTML, CSS, and JavaScript.
WEB_DIR = Path(__file__).parent / "web"


class NotesHandler(BaseHTTPRequestHandler):

    def send_json(self, status, data):
        """Send a JSON response to the browser."""
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path

        # API: return all notes as JSON.
        if path == "/api/notes":
            self.send_json(200, {"notes": db.list_notes()})
            return

        # Serve the main page and its static assets.
        files = {
            "/": "index.html",
            "/style.css": "style.css",
            "/app.js": "app.js",
        }

        filename = files.get(path)

        if filename is None:
            self.send_json(404, {"error": "Not found"})
            return

        content = (WEB_DIR / filename).read_bytes()

        content_types = {
            "index.html": "text/html; charset=utf-8",
            "style.css": "text/css; charset=utf-8",
            "app.js": "text/javascript; charset=utf-8",
        }

        self.send_response(200)
        self.send_header("Content-Type", content_types[filename])
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_POST(self):
        path = urlparse(self.path).path

        if path != "/api/notes":
            self.send_json(404, {"error": "Not found"})
            return

        # Read the JSON body sent by the browser.
        try:
            length = int(self.headers.get("Content-Length", "0"))

            if length <= 0 or length > 10_000:
                self.send_json(400, {"error": "Invalid request size"})
                return

            payload = json.loads(self.rfile.read(length))
        except (ValueError, json.JSONDecodeError):
            self.send_json(400, {"error": "Invalid JSON"})
            return

        # Validate the fields before writing to the database.
        if not isinstance(payload, dict):
            self.send_json(400, {"error": "Expected a JSON object"})
            return

        title = payload.get("title")
        body = payload.get("body")

        if not isinstance(title, str) or not isinstance(body, str):
            self.send_json(400, {"error": "Title and body must be text"})
            return

        title = title.strip()
        body = body.strip()

        if not title or not body:
            self.send_json(400, {"error": "Title and body are required"})
            return

        if len(title) > 200 or len(body) > 5000:
            self.send_json(400, {"error": "Note is too long"})
            return

        note_id = db.create_note(title, body)
        self.send_json(201, {"id": note_id})

    def do_DELETE(self):
        path = urlparse(self.path).path
        parts = path.split("/")

        # Expected URL: /api/notes/123
        if len(parts) != 4 or parts[:3] != ["", "api", "notes"]:
            self.send_json(404, {"error": "Not found"})
            return

        try:
            note_id = int(parts[3])
            if note_id <= 0:
                raise ValueError
        except ValueError:
            self.send_json(400, {"error": "Invalid note ID"})
            return

        if db.delete_note(note_id):
            self.send_json(200, {"deleted": True})
        else:
            self.send_json(404, {"error": "Note not found"})


if __name__ == "__main__":
    db.init_db()

    # ThreadingHTTPServer can handle multiple requests concurrently.
    host = "0.0.0.0"
    port = int(os.environ.get("PORT", "8000"))
    server = ThreadingHTTPServer((host, port), NotesHandler)

    print("Mini Notes running at http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server.")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server...")
    finally:
        server.server_close()
