"""OAuth 2.0 flow with built-in pywebview browser."""

import threading
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import uuid

# Will be set by the browser
_webview_result = {"access_token": "", "refresh_token": "", "expires_in": "", "error": ""}
_webview_event = threading.Event()


def start_auth_flow(
    auth_url: str,
    token_url: str,
    client_id: str,
    client_secret: str,
    redirect_uri: str,
    scope: str,
    extra_params: dict | None = None,
) -> dict:
    """
    Run OAuth flow with built-in browser window.
    Returns dict: {access_token, refresh_token, expires_in, error}
    """
    global _webview_result, _webview_event
    _webview_result = {"access_token": "", "refresh_token": "", "expires_in": "", "error": ""}
    _webview_event = threading.Event()

    state = uuid.uuid4().hex

    # Build auth URL
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope,
        "state": state,
    }
    if extra_params:
        params.update(extra_params)

    # Find free port for callback server
    port = None
    for p in range(18233, 18400):
        try:
            s = HTTPServer(("127.0.0.1", p), _make_handler())
            port = p
            break
        except OSError:
            continue

    if not port:
        return {"error": "No free port for OAuth callback"}

    actual_redirect = f"http://127.0.0.1:{port}/callback"
    params["redirect_uri"] = actual_redirect
    auth_full = f"{auth_url}?{urllib.parse.urlencode(params)}"

    # Start callback server in background
    server_thread = threading.Thread(target=s.serve_forever, daemon=True)
    server_thread.start()

    # Open built-in browser
    import webview
    window = webview.create_window(
        "aLCloud — Авторизация",
        auth_full,
        width=500,
        height=700,
        resizable=True,
        min_size=(400, 500),
    )

    def on_closed():
        if not _webview_event.is_set():
            _webview_result["error"] = "Окно закрыто без авторизации"
            _webview_event.set()

    window.events.closed += on_closed

    def start_browser():
        webview.start()

    browser_thread = threading.Thread(target=start_browser, daemon=True)
    browser_thread.start()

    # Wait for callback (max 300s)
    _webview_event.wait(timeout=300)
    s.shutdown()

    return dict(_webview_result)


def _make_handler():
    global _webview_result, _webview_event

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            global _webview_result, _webview_event
            query = urllib.parse.urlparse(self.path).query
            qs = urllib.parse.parse_qs(query)

            if "error" in qs:
                _webview_result["error"] = qs["error"][0]
                self._respond("Ошибка авторизации")
            elif qs.get("code"):
                code = qs["code"][0]
                token_data = _exchange_token(
                    self.server.token_url,
                    self.server.client_id,
                    self.server.client_secret,
                    code,
                    self.server.redirect_uri,
                )
                _webview_result.update(token_data)
                self._respond("Авторизация успешна! Можно закрыть это окно.")
            else:
                self._respond("Загрузка...")

            _webview_event.set()

        def _respond(self, msg):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(f"""
                <html><body style="display:flex;justify-content:center;align-items:center;
                height:100vh;font-family:system-ui;background:#1a1a2e;color:#eee;margin:0">
                <div style="text-align:center">
                <h2>{msg}</h2>
                <p style="margin-top:20px;color:#888">Вы можете закрыть это окно</p>
                </div></body></html>
            """.encode())

        def log_message(self, *_):
            pass

    # Attach data to server instance
    orig_init = Handler.__init__

    def new_init(self, *a, **kw):
        orig_init(self, *a, **kw)

    Handler.__init__ = new_init
    return Handler


def _exchange_token(token_url, client_id, client_secret, code, redirect_uri) -> dict:
    try:
        resp = requests.post(
            token_url,
            data={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "client_secret": client_secret,
                "code": code,
                "redirect_uri": redirect_uri,
            },
            headers={"Accept": "application/json"},
            timeout=15,
        )
        data = resp.json()
        return {
            "access_token": data.get("access_token", ""),
            "refresh_token": data.get("refresh_token", ""),
            "expires_in": str(data.get("expires_in", "")),
            "error": data.get("error_description", data.get("error", "")),
        }
    except Exception as e:
        return {"error": str(e)}
