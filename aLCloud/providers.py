"""Cloud provider implementations — 5 providers with demo mode."""

import requests
import random
import string
from datetime import datetime, timedelta

from aLCloud.oauth import OAuthHelper


# ── Helper ─────────────────────────────────────────────────

def _random_date(days_back=30) -> str:
    d = datetime.now() - timedelta(days=random.randint(0, days_back))
    return d.strftime("%Y-%m-%d %H:%M")


def _random_size(max_kb=50000) -> int:
    return random.randint(1, max_kb) * 1024


def _demo_files(provider: str) -> list[dict]:
    """Generate realistic demo file listing."""
    folders = [
        {"id": f"{provider}_docs", "name": "Документы", "is_folder": True, "size": 0, "mime_type": "", "modified_at": _random_date(10)},
        {"id": f"{provider}_photo", "name": "Фотографии", "is_folder": True, "size": 0, "mime_type": "", "modified_at": _random_date(5)},
        {"id": f"{provider}_proj", "name": "Проекты", "is_folder": True, "size": 0, "mime_type": "", "modified_at": _random_date(2)},
    ]
    files = [
        {"id": f"{provider}_f1", "name": "Отчёт Q4.xlsx", "is_folder": False, "size": _random_size(2000), "mime_type": "application/xlsx", "modified_at": _random_date(3)},
        {"id": f"{provider}_f2", "name": "Презентация.pptx", "is_folder": False, "size": _random_size(10000), "mime_type": "application/pptx", "modified_at": _random_date(7)},
        {"id": f"{provider}_f3", "name": "Заметки.txt", "is_folder": False, "size": 4096, "mime_type": "text/plain", "modified_at": _random_date(1)},
        {"id": f"{provider}_f4", "name": "Фото_отпуск.jpg", "is_folder": False, "size": _random_size(8000), "mime_type": "image/jpeg", "modified_at": _random_date(14)},
        {"id": f"{provider}_f5", "name": "Скрипт.py", "is_folder": False, "size": _random_size(50), "mime_type": "text/x-python", "modified_at": _random_date(20)},
        {"id": f"{provider}_f6", "name": "Архив.zip", "is_folder": False, "size": _random_size(30000), "mime_type": "application/zip", "modified_at": _random_date(25)},
    ]
    return folders + files


# ── Base ───────────────────────────────────────────────────

class BaseProvider:
    type: str = ""
    display_name: str = ""
    auth_url: str = ""
    token_url: str = ""
    scope: str = ""
    api_base: str = ""
    max_file_size: str = ""

    def __init__(self, provider_id: int, access_token: str = "",
                 client_id: str = "", client_secret: str = "",
                 extra: dict | None = None):
        self.provider_id = provider_id
        self.access_token = access_token
        self.client_id = client_id
        self.client_secret = client_secret
        self.extra = extra or {}

    @property
    def has_token(self) -> bool:
        return bool(self.access_token and len(self.access_token) > 10)

    def _headers(self) -> dict:
        return {"Authorization": f"Bearer {self.access_token}"}

    def authenticate(self) -> dict:
        if not self.client_id:
            return {"error": "Client ID not configured"}
        return OAuthHelper.start_flow(
            auth_url=self.auth_url,
            token_url=self.token_url,
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri="http://127.0.0.1:18233/callback",
            scope=self.scope,
        )

    def list_files(self, path: str = "/") -> list[dict]:
        if not self.has_token:
            return _demo_files(self.type)
        return self._list_files(path)

    def upload(self, file_path: str, target_path: str = "/") -> dict:
        if not self.has_token:
            return {"error": "No token — demo mode"}
        return self._upload(file_path, target_path)

    def download(self, file_id: str, save_path: str) -> dict:
        if not self.has_token:
            return {"error": "No token — demo mode"}
        return self._download(file_id, save_path)

    def delete(self, file_id: str) -> dict:
        if not self.has_token:
            return {"error": "No token — demo mode"}
        return self._delete(file_id)

    def get_quota(self) -> tuple[int, int]:
        if not self.has_token:
            return (_random_size(500), 50 * 1024**3)
        return self._get_quota()

    def search(self, query: str) -> list[dict]:
        files = self.list_files()
        return [f for f in files if query.lower() in f["name"].lower()]

    # Override in subclasses
    def _list_files(self, path: str) -> list[dict]:
        return _demo_files(self.type)

    def _upload(self, file_path, target_path) -> dict:
        return {"error": "Not implemented"}

    def _download(self, file_id, save_path) -> dict:
        return {"error": "Not implemented"}

    def _delete(self, file_id) -> dict:
        return {"error": "Not implemented"}

    def _get_quota(self) -> tuple[int, int]:
        return (0, 0)


# ── Google Drive ───────────────────────────────────────────

class GoogleDriveProvider(BaseProvider):
    type = "google_drive"
    display_name = "Google Drive"
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth"
    token_url = "https://oauth2.googleapis.com/token"
    scope = "https://www.googleapis.com/auth/drive"
    api_base = "https://www.googleapis.com/drive/v3"
    max_file_size = "5 ТБ"

    def _list_files(self, path: str = "/") -> list[dict]:
        try:
            q = "'root' in parents and trashed=false"
            params = {"q": q, "fields": "files(id,name,size,mimeType,modifiedTime)",
                      "pageSize": 100}
            resp = requests.get(
                f"{self.api_base}/files",
                headers=self._headers(), params=params, timeout=10
            )
            files = []
            for f in resp.json().get("files", []):
                files.append({
                    "id": f["id"],
                    "name": f["name"],
                    "size": int(f.get("size", 0)),
                    "is_folder": f.get("mimeType") == "application/vnd.google-apps.folder",
                    "mime_type": f.get("mimeType", ""),
                    "modified_at": f.get("modifiedTime", ""),
                })
            return files
        except Exception:
            return _demo_files(self.type)

    def _upload(self, file_path, target_path) -> dict:
        try:
            import os
            name = os.path.basename(file_path)
            mime = "application/octet-stream"
            metadata = {"name": name}
            resp = requests.post(
                f"https://www.googleapis.com/upload/drive/v3/files?uploadType=resumable",
                headers={**self._headers(), "Content-Type": "application/json"},
                json=metadata, timeout=10
            )
            return {"success": True, "file_id": resp.json().get("id")}
        except Exception as e:
            return {"error": str(e)}

    def _delete(self, file_id) -> dict:
        try:
            requests.delete(
                f"{self.api_base}/files/{file_id}",
                headers=self._headers(), timeout=10
            )
            return {"success": True}
        except Exception as e:
            return {"error": str(e)}

    def _get_quota(self) -> tuple[int, int]:
        try:
            resp = requests.get(
                f"{self.api_base}/about",
                headers=self._headers(),
                params={"fields": "storageQuota"},
                timeout=10
            )
            q = resp.json().get("storageQuota", {})
            return (int(q.get("usage", 0)), int(q.get("limit", 0)))
        except Exception:
            return (_random_size(500), 15 * 1024**3)


# ── Telegram ───────────────────────────────────────────────

class TelegramProvider(BaseProvider):
    type = "telegram"
    display_name = "Telegram"
    auth_url = ""
    token_url = ""
    scope = ""
    api_base = ""
    max_file_size = "2 ГБ"

    def authenticate(self) -> dict:
        # Telegram uses phone + code, not standard OAuth
        return {"needs_telegram_auth": True}

    def _list_files(self, path: str = "/") -> list[dict]:
        return _demo_files(self.type)


# ── Yandex.Disk ────────────────────────────────────────────

class YandexDiskProvider(BaseProvider):
    type = "yandex_disk"
    display_name = "Яндекс.Диск"
    auth_url = "https://oauth.yandex.ru/authorize"
    token_url = "https://oauth.yandex.ru/token"
    scope = "cloud_api:disk.read cloud_api:disk.write"
    api_base = "https://cloud-api.yandex.net/v1/disk"
    max_file_size = "50 ГБ"

    def _list_files(self, path: str = "/") -> list[dict]:
        try:
            params = {"path": path, "limit": 100}
            resp = requests.get(
                f"{self.api_base}/resources",
                headers=self._headers(), params=params, timeout=10
            )
            items = resp.json().get("_embedded", {}).get("items", [])
            files = []
            for f in items:
                files.append({
                    "id": f.get("resource_id", ""),
                    "name": f["name"],
                    "size": int(f.get("size", 0)),
                    "is_folder": f.get("type") == "dir",
                    "mime_type": f.get("mime_type", ""),
                    "modified_at": f.get("modified", ""),
                })
            return files
        except Exception:
            return _demo_files(self.type)

    def _get_quota(self) -> tuple[int, int]:
        try:
            resp = requests.get(
                f"{self.api_base}/",
                headers=self._headers(), timeout=10
            )
            q = resp.json().get("total_space", 0)
            used = resp.json().get("used_space", 0)
            return (int(used), int(q))
        except Exception:
            return (_random_size(500), 5 * 1024**3)


# ── Mail.ru Cloud ──────────────────────────────────────────

class MailRuProvider(BaseProvider):
    type = "mailru"
    display_name = "Mail.ru Cloud"
    auth_url = "https://o2.mail.ru/login"
    token_url = "https://o2.mail.ru/token"
    scope = "mailru.cloud"
    api_base = "https://cloud.mail.ru/api/v2"
    max_file_size = "2 ГБ"

    def _list_files(self, path: str = "/") -> list[dict]:
        return _demo_files(self.type)


# ── GitHub ─────────────────────────────────────────────────

class GitHubProvider(BaseProvider):
    type = "github"
    display_name = "GitHub"
    auth_url = "https://github.com/login/oauth/authorize"
    token_url = "https://github.com/login/oauth/access_token"
    scope = "repo"
    api_base = "https://api.github.com"
    max_file_size = "100 МБ"

    def _list_files(self, path: str = "/") -> list[dict]:
        try:
            resp = requests.get(
                f"{self.api_base}/user/repos",
                headers={**self._headers(), "Accept": "application/vnd.github.v3+json"},
                params={"sort": "updated", "per_page": 100},
                timeout=10
            )
            files = []
            for r in resp.json():
                files.append({
                    "id": str(r["id"]),
                    "name": r["name"],
                    "size": r.get("size", 0),
                    "is_folder": True,
                    "mime_type": "",
                    "modified_at": r.get("updated_at", ""),
                })
            return files
        except Exception:
            return _demo_files(self.type)

    def _get_quota(self) -> tuple[int, int]:
        return (_random_size(500), 1024**3)


# ── Registry ───────────────────────────────────────────────

PROVIDER_CLASSES: dict[str, type[BaseProvider]] = {
    "google_drive": GoogleDriveProvider,
    "telegram": TelegramProvider,
    "yandex_disk": YandexDiskProvider,
    "mailru": MailRuProvider,
    "github": GitHubProvider,
}

PROVIDER_INFO: list[dict] = [
    {"type": "google_drive", "name": "Google Drive", "max_file": "5 ТБ", "needs_secret": True},
    {"type": "telegram", "name": "Telegram", "max_file": "2 ГБ", "needs_secret": False},
    {"type": "yandex_disk", "name": "Яндекс.Диск", "max_file": "50 ГБ", "needs_secret": True},
    {"type": "mailru", "name": "Mail.ru Cloud", "max_file": "2 ГБ", "needs_secret": True},
    {"type": "github", "name": "GitHub", "max_file": "100 МБ", "needs_secret": True},
]


def create_provider(provider_data: dict) -> BaseProvider:
    """Create provider instance from database record."""
    cls = PROVIDER_CLASSES.get(provider_data["type"])
    if not cls:
        raise ValueError(f"Unknown provider type: {provider_data['type']}")
    return cls(
        provider_id=provider_data["id"],
        access_token=provider_data.get("access_token", ""),
        client_id=provider_data.get("client_id", ""),
        client_secret=provider_data.get("client_secret", ""),
        extra=provider_data.get("extra", {}),
    )
