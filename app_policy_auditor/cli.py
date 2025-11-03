from pathlib import Path
from typing import Optional, List
import sys
import typer
from . import __version__
from .discovery.web import discovery_policy_urls
from .fetch.http import HttpFetcher

app = typer.Typer(add_completion=False, help="Audit privacy policies and EULAs for risk signals.")

@app.command()
def version():
    """Print version and exit."""
    typer.echo(__version__)

@app.command()
def scan(
    seed: Optional[Path] = typer.Option(None, help="Seed file with one target per line"),
    include_terms: bool = typer.Option(False, help="Include Terms/EULA discovery"),
    out: Path = typer.Option(Path("report"), help="Output directory for cached docs"),
    max_urls: int = typer.Option(2, help="Max policy URLs per target"),
):
    """Discover -> fetch and cache docs."""
    out.mkdir(parents=True, exist_ok=True)
    cache_dir = out / "policies"
    cache_dir.mkdir(parents=True, exist_ok=True)

    targets: List[str] = []
    if seed and seed.exists():
        targets = [t.strip() for t in seed.read_text(encoding="utf-8").splitlines() if t.strip() and not t.startswith("#")]
    if not targets:
        typer.echo("No targets provided. Use --seed to supply domains or org names.")
        raise typer.Exit(code=2)

    fetcher = HttpFetcher(cache_root=cache_dir)
    total_fetched = 0

    for target in targets:
        urls = discover_policy_urls(target, include_terms=include_terms, max_urls=max_urls)
        if not urls:
            typer.echo(f"[skip] No policy URLs found for: {target}")
            continue
        for url in urls:
            resp = fetcher.get(url)
            if resp.status == "cached":
                typer.echo(f"[cached] {url}")
            elif resp.status == "fetched":
                typer.echo(f"[fetch] {url} (etag={resp.etag or '-'} lastmode={resp.last_modified or '-'})")
                total_fetched += 1
            elif resp.status == "not-modified":
                typer.echo(f"[304 ] {url}")
            else:
                typer.echo(f"[err ] {url} {resp.error}")
    typer.echo(f"Done. New documents fetched: {total_fetched}. Cached at {cache_dir.resolve()}")

    if __name__ == "__main__":
        app()
