"""Minimal web service for the delivery pipeline: standard library only, so the image stays small
and the dependency scan has almost nothing to flag."""
import json
import os
import signal
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

VERSION = os.environ.get("APP_VERSION", "dev")
MESSAGE = os.environ.get("APP_MESSAGE", "Hello from ECS Fargate")


class Handler(BaseHTTPRequestHandler):
    server_version = "app"
    sys_version = ""

    def _send(self, code, body, ctype="application/json"):
        data = body.encode()
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/health":
            self._send(200, json.dumps({"status": "ok", "version": VERSION}))
        elif self.path == "/":
            self._send(200, json.dumps({"message": MESSAGE, "version": VERSION}))
        else:
            self._send(404, json.dumps({"error": "not found"}))

    def log_message(self, fmt, *args):  # structured logs to stdout for CloudWatch
        sys.stdout.write(json.dumps({"client": self.client_address[0], "request": fmt % args}) + "\n")
        sys.stdout.flush()


def main():
    port = int(os.environ.get("PORT", "8080"))
    httpd = ThreadingHTTPServer(("0.0.0.0", port), Handler)
    signal.signal(signal.SIGTERM, lambda *_: httpd.shutdown())  # ECS stops tasks with SIGTERM
    print(json.dumps({"event": "start", "port": port, "version": VERSION}), flush=True)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
