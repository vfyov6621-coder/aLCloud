"""OAuth 2.0 flow: open browser, run local HTTP server, catch callback."""

import webbrowser
import threading
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests
import uuid


class OAuthHelper:

    @staticmethod
    def start_flow(
        auth_url: str,
        token_url: str,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scope: str,
        code_key: str = "code",
        extra_params: dict | None = None,
    ) -> dict:
        """
        Run OAuth flow.
        Returns dict: {access_token, refresh_token, expires_in, error}
        """
        state = uuid.uuid4().hex
        result: dict = {"access_token": "", "refresh_token": "", "expires_in": "", "error": ""}
        received = threading.Event()

        # Build authorization URL
        params = {
            "client_id": client_id,
            "redirect_uri": redirect_uri,
            "response_type": "code",
            "scope": scope,
            "state": state,
        }
        if extra_params:
            params.update(extra_params)
        auth_full = f"{auth_url}?{urllib.parse.urlencode(params)}"

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                query = urllib.parse.urlparse(self.path).query
                qs = urllib.parse.parse_qs(query)

                if "error" in qs:
                    result["error"] = qs["error"][0]
                    self._respond("Authorization failed")
                elif qs.get("code"):
                    code = qs["code"][0]
                    token_data = OAuthHelper._exchange_token(
                        token_url, client_id, client_secret, code, redirect_uri
                    )
                    result.update(token_data)
                    self._respond("Authorization successful! You can close this tab.")
                else:
                    self._respond("Waiting...")

                received.set()

            def _respond(self, msg):
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                html = f"""<html><body style="display:flex;justify-content:center;align-items:center;
                height:100vh;font-family:system-ui;background:#1a1a2e;color:#eee">
                <h2>{msg}</h2></body></html>"""
                self.wfile.write(html.encode())

            def log_message(self, *_):
                pass

        # Find free port
        port = 18233
        for p in range(18233, 18300):
            try:
                s = HTTPServer(("127.0.0.1", p), Handler)
                port = p
                break
            except OSError:
                continue
        else:
            return {"error": "No free port for OAuth callback"}

        actual_redirect = f"http://127.0.0.1:{port}/callback"
        # Rebuild auth URL with actual port
        params["redirect_uri"] = actual_redirect
        auth_full = f"{auth_url}?{urllib.parse.urlencode(params)}"

        # Start server in background
        server_thread = threading.Thread(target=s.serve_forever, daemon=True)
        server_thread.start()

        # Open browser
        webbrowser.open(auth_full)

        # Wait for callback (max 120s)
        received.wait(timeout=120)
        s.shutdown()

        return result

    @staticmethod
    def _exchange_token(
        token_url: str,
        client_id: str,
        client_secret: str,
        code: str,
        redirect_uri: str,
    ) -> dict:
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
