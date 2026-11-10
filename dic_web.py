"""Web page for dic.py (Dictator in Diapers / Dittatore in Culla).

Start:  python3 dic_web.py
The browser opens on http://localhost:8000 by itself.
Only Python's standard library is needed (portraits come from Wikimedia,
so an internet connection is needed to see them).
"""
import json
import webbrowser
from datetime import date
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlsplit

import dic

PAGE = Path(__file__).with_name("dic_web.html")
FONT_DIR = Path(__file__).with_name("fonts")   # licensed fonts go here (.woff2, .woff, .otf, .ttf)
FONT_TYPES = {".woff2": "font/woff2", ".woff": "font/woff", ".otf": "font/otf", ".ttf": "font/ttf"}
PORT = 8000


class Handler(BaseHTTPRequestHandler):
    def _reply(self, code, body, content_type):
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlsplit(self.path).path  # ignore any ?query in the address
        if path in ("/", "/index.html"):
            self._reply(200, PAGE.read_text(encoding="utf-8"), "text/html")
        elif path == "/api/fonts":
            found = sorted(f.name for f in FONT_DIR.glob("*") if f.suffix.lower() in FONT_TYPES) \
                if FONT_DIR.is_dir() else []
            self._reply(200, json.dumps(found), "application/json")
        elif path.startswith("/fonts/"):
            self._send_font(unquote(path.removeprefix("/fonts/")))
        else:
            self._reply(404, "Not found", "text/plain")

    def _send_font(self, name):
        file = FONT_DIR / name
        # only files directly inside the fonts folder, no paths like ../
        if "/" in name or "\\" in name or file.suffix.lower() not in FONT_TYPES or not file.is_file():
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()
            return
        data = file.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", FONT_TYPES[file.suffix.lower()])
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "max-age=3600")
        self.end_headers()
        self.wfile.write(data)

    def do_POST(self):
        if urlsplit(self.path).path != "/api/compute":
            self._reply(404, "Not found", "text/plain")
            return
        try:
            length = int(self.headers.get("Content-Length", 0))
            request = json.loads(self.rfile.read(length))
            lang = request.get("lang", "it")
            parents = [
                (p["name"].strip() or f"Parent {i + 1}", date.fromisoformat(p["date"]))
                for i, p in enumerate(request["parents"][:2])
            ]
            # No date = "not sure yet": compute() uses today + 9 months
            child = request.get("child")
            child_birth = date.fromisoformat(child) if child else None
            result = dic.compute(parents, child_birth, lang)
        except (KeyError, ValueError, TypeError) as e:
            self._reply(400, json.dumps({"error": f"Invalid data: {e}"}), "application/json")
            return
        self._reply(200, json.dumps(result, ensure_ascii=False), "application/json")

    def log_request(self, code="-", size="-"):
        # Only failed requests (4xx and 5xx) are printed in the terminal
        if isinstance(code, int) and code >= 400:
            super().log_request(code, size)


def main():
    for port in range(PORT, PORT + 20):
        try:
            server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
            break
        except OSError:
            continue
    else:
        raise SystemExit("No free port between 8000 and 8019")

    url = f"http://localhost:{port}"
    print(f"Dictator in Diapers is running on {url}  (Ctrl+C to stop)")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
