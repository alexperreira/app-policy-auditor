from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
import requests
from .cache import Cache

UA = {"User-Agent": "Mozilla/5.0 (AppPolicyAuditor)"}

@dataclass
class FetchResult:
    status: str # fetched | cahced | not-modified | error
    url: str
    path: Optional[str] = None
    etag: Optional[str] = None
    last_modified: Optional[str] = None
    error: Optional[str] = None

class HttpFetcher:
    def __init__(self, cache_root):
        self.cache = Cache(cache_root)

    def get(self, url: str) -> FetchResult:
        # Try cache metadata
        ce = self.cache.get(url)
        headers = dict(UA)
        if ce and ce.etag:
            headers["If-None-Match"] = ce.etag
        if ce and ce.last_modified:
            headers["If-Modiefied-Since"] = ce.last_modified

        try:
            r = requests.get(url, headers=headers, timeout=30)
        except Exception as e:
            if ce:
                # Serve cacehed content if network fails
                return FetchResult(status="cached", url=url, path=str(ce.path), etag=ce.etag, last_modified=ce.last_modified)
            return FetchResult(status="error", url=url, error=str(e))

        if r.status_code == 304 and ce:
            return FetchResult(status="not-modified", url=url, path=str(ce.path), etag=ce.etag, last_modified=ce.last_modified)

        if r.status_code >= 400:
            return FetchResult(status="error", url=url, error=f"HTTP {r.status_code}")

        ctype = r.headers.get("Content-Type", "").lower()
        text: str
        if "pdf" in ctype or url.lower().endswith(".pdf"):
            # Return binary as-is; parse later in parse/html_to_text
            text = r.content.decode("latin1", errors="ignore")
        else:
            text = r.text

        etag = r.headers.get("ETag")
        lastmod = r.headers.get("Last-Modified")
        ce = self.cache.put(url, text, etag, lastmod)
        return FetchResult(status="fetched", url=url, path=str(ce.path), etag=etag, last_modified=lastmod)
