"""RoboGuard local demo server and Ollama-backed diagnostic endpoint."""
import json
import os
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.error import URLError
from urllib.request import Request, urlopen

ROOT = os.path.dirname(os.path.abspath(__file__))
OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
MODEL = os.environ.get("OLLAMA_MODEL", "gemma3:1b")


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def send_json(self, status, data):
        payload = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_GET(self):
        if self.path == "/api/health":
            self.send_json(200, {"service": "roboguard", "model": MODEL})
            return
        super().do_GET()

    def do_POST(self):
        if self.path != "/api/analyze":
            self.send_json(404, {"error": "Not found"})
            return
        try:
            data = json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))))
            telemetry = data.get("telemetry", {})
            prompt = (
                "You are a cautious robotics maintenance assistant. Explain this telemetry in "
                "2-4 concise sentences: identify the strongest likely cause, cite the readings, "
                "give one safe next inspection, and state uncertainty. Never claim certainty or "
                "instruct operation of unsafe equipment. Do not invent readings.\n"
                f"Robot: {data.get('robot', 'unknown')}\nTelemetry: "
                f"{json.dumps(telemetry)}\nTrend: {data.get('recent_trend', '')}"
            )
            request = Request(
                f"{OLLAMA_URL.rstrip('/')}/api/chat",
                data=json.dumps({
                    "model": MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "options": {"temperature": 0.2},
                }).encode(),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urlopen(request, timeout=90) as response:
                result = json.loads(response.read())
            diagnosis = result.get("message", {}).get("content", "").strip()
            if not diagnosis:
                raise ValueError("The model returned an empty response")
            self.send_json(200, {"diagnosis": diagnosis, "model": MODEL, "provider": "Ollama"})
        except (URLError, TimeoutError, OSError) as exc:
            self.send_json(503, {"error": f"Could not reach Ollama at {OLLAMA_URL}: {exc}"})
        except (ValueError, json.JSONDecodeError) as exc:
            self.send_json(400, {"error": f"Invalid request or model response: {exc}"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    print(f"RoboGuard at http://localhost:{port} · model {MODEL} · Ollama {OLLAMA_URL}")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
