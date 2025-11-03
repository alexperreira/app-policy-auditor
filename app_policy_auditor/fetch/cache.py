from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import hashlib, json
from typing import Optional

META_FILE = "index.json"

@dataclass
class CacheEntry:
    url: str
    path: Path
    etag: Optional[str] = None
    last_modified: Optional[str] = None

class Cache:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.meta_path = self.root / META_FILE
        self._meta = {}
        if self.meta_path.exists():
            try:
                self._meta = json.loads(self.meta_path.read_text(encoding="utf-8"))
            except Exception:
                self._meta = {}

    def _key(self, url: str) -> str:
        return hashlib.sha1(url.encode("utf-8")).hexdigest()

    def path_for(self, url: str) -> Path:
        return self.root / f"{self._key(url)}.txt"

    def get(self, url: str) -> Optional[CacheEntry]:
        key = self._key(url)
        meta = self._meta.get(key)
        p = self.path_for(url)
        if not meta or not p.exists():
            return None
        return CacheEntry(url=url, path=p, etag=meta.get("etag"), last_modified=meta.get("last_modified"))

    def put(self, url: str, content: str, etag: Optional[str], last_modified: Optional[str]) -> CacheEntry:
        p = self.path_for(url)
        p.write_text(content, encoding="utf-8")
        key = self._key(url)
        self._meta[key] = {"etag": etag, "last_modified": last_modified}
        self.meta_path.write_text(json.dumps(self._meta, ensure_ascii=False, indent=2), encoding="utf-8")
        return CacheEntry(url=url, path=p, etag=etag, last_modified=last_modified)