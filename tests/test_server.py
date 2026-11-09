import json
import pathlib
import sys
import threading
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "app"))
import server  # noqa: E402


@pytest.fixture(scope="module")
def base():
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()


def get(url):
    try:
        r = urllib.request.urlopen(url, timeout=5)
        return r.status, dict(r.headers), json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), json.loads(e.read())


def test_health(base):
    code, headers, body = get(base + "/health")
    assert code == 200 and body["status"] == "ok"
    assert headers["X-Content-Type-Options"] == "nosniff"


def test_root(base):
    assert get(base + "/")[2]["message"]


def test_unknown_path_404(base):
    assert get(base + "/admin")[0] == 404
