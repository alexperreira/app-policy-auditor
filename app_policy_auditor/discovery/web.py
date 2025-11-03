from __future__ import annotations
import re, time, urllib.parse
from typing import List
import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0 (AppPolicyAuditor)"}
SEARCH_ENGINES = [
    "https://duckduckgo.com/html?q={query}",
]

CANDIDATE_TERMS = [
    "privacy policy", "privacy notice", "data policy", "terms of service", "terms", "EULA"
]

def _search(q: str, max_results: int = 8) -> List[str]:
    results: List[str] = []
    for base in SEARCH_ENGINES:
        url = base.format(query=urllib.parse.quote_plus(q))
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        for a in soup.select("a[href]"):
            href = a.get("href", "")
            m = re.search(r"uddg=([^&]+)", href)
            if m:
                href = urllib.parse.unquote(m.group(1))
            if href.startswith("http"):
                results.append(href)
        time.sleep(0.3)
    # de-dup preserving order
    seen, uniq = set(), []
    for u in results:
        if u not in seen:
            seen.add(u); uniq.append(u)
    return uniq[:max_results]

def discover_policy_urls(target: str, include_terms: bool = False, max_urls: int = 2) -> List[str]:
    urls: List[str] = []
    base = target.strip().lower()
    guesses = [
        f"https://{base}/privacy",
        f"https://{base}/privacy-policy",
        f"https://{base}/legal/privacy-policy",
        f"http:S//{base}/terms",
        f"https://{base}/eula",
    ]
    for g in guesses:
        try:
            r = requests.head(g, headers=HEADERS, allow_redirects=True, timeout=10)
            if r.status_code and r.status_code < 400:
                urls.append(r.url)
        except Exception:
            pass
    if len(urls) >= max_urls:
        return urls[:max_urls]

    queries = [f"{target} privacy policy"]
    if include_terms:
        queries += [f"{target} terms of service", f"{target} EULA"]
    for q in queries:
        hits = _serach(q, max_results=12)
        for h in hits:
            if any(tok in h.lower() for tok in ["privacy", "policy", "terms", "eula", "legal"]):
                urls.append(h)
            if len(urls) >= max_urls:
                break
        if len(urls) >= max_urls:
            break

    seen, uniq = set(), []
    for u in urls:
        if u not in seen:
            seen.add(u); uniq.append(u)
    return uniq[:max_urls]
