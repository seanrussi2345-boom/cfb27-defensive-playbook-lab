#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
from bs4 import BeautifulSoup

from audit_play_art import (
    HEADERS,
    ROOT,
    OUT,
    download,
    extract_routes,
    image_candidates,
    script_signals,
    slugify,
)

INPUT = ROOT / "audit-batch-input.json"


def audit_play(formation: str, formation_slug: str, play: str) -> dict:
    pslug = slugify(play)
    url = f"https://collegefootball.gg/plays/{formation_slug}/{pslug}/"
    item = {"play": play, "slug": pslug, "url": url}
    session = requests.Session()
    try:
        response = session.get(url, headers=HEADERS, timeout=35)
        item.update(
            status=response.status_code,
            final_url=response.url,
            html_bytes=len(response.content),
        )
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            item["title"] = soup.title.get_text(" ", strip=True) if soup.title else None
            item["routes"] = extract_routes(soup)
            item["image_candidates"] = image_candidates(soup, response.url, play)[:12]
            item["script_signals"] = script_signals(soup)
            item["html_sha256"] = hashlib.sha256(response.content).hexdigest()
            outdir = OUT / formation_slug
            outdir.mkdir(parents=True, exist_ok=True)
            img_path, img_url, content_type, size, errors = download(
                session, item["image_candidates"], outdir / pslug
            )
            item.update(
                image_path=img_path,
                image_url=img_url,
                image_content_type=content_type,
                image_bytes=size,
                image_errors=errors,
            )
    except Exception as exc:
        item["error"] = repr(exc)
    finally:
        session.close()
    item["ok"] = item.get("status") == 200 and bool(item.get("image_path"))
    return item


def audit_formation(config: dict) -> dict:
    formation = config["formation"]
    formation_slug = config["formation_slug"]
    plays = config["plays"]
    report = {
        "formation": formation,
        "formation_slug": formation_slug,
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "plays": [],
    }

    workers = min(8, max(1, len(plays)))
    results = [None] * len(plays)
    with ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {
            executor.submit(audit_play, formation, formation_slug, play): index
            for index, play in enumerate(plays)
        }
        for future in as_completed(futures):
            index = futures[future]
            results[index] = future.result()

    report["plays"] = results
    report["passed"] = sum(1 for item in results if item.get("ok"))
    report["failed"] = len(results) - report["passed"]

    (OUT / f"{formation_slug}.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )
    summary = [f"# Play-art audit: {formation}", ""]
    for item in results:
        summary.append(
            f'- **{item["play"]}** — HTTP {item.get("status")} — '
            f'routes {len(item.get("routes", []))} — '
            f'image `{item.get("image_path") or "missing"}`'
        )
    (OUT / f"{formation_slug}.md").write_text(
        "\n".join(summary) + "\n", encoding="utf-8"
    )
    return {
        "formation": formation,
        "formation_slug": formation_slug,
        "total": len(results),
        "passed": report["passed"],
        "failed": report["failed"],
        "failed_plays": [
            item["play"] for item in results if not item.get("ok")
        ],
    }


def main() -> None:
    config = json.loads(INPUT.read_text(encoding="utf-8"))
    combined = {
        "batch": config.get("batch", "batch"),
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "formations": [],
    }
    for index, formation in enumerate(config["formations"], 1):
        print(
            f'[{index}/{len(config["formations"])}] '
            f'Auditing {formation["formation"]} '
            f'({len(formation["plays"])} plays)'
        )
        combined["formations"].append(audit_formation(formation))

    combined["total_plays"] = sum(item["total"] for item in combined["formations"])
    combined["passed"] = sum(item["passed"] for item in combined["formations"])
    combined["failed"] = sum(item["failed"] for item in combined["formations"])
    (OUT / "nickel-final-reconciliation.json").write_text(
        json.dumps(combined, indent=2), encoding="utf-8"
    )

    lines = [
        "# Nickel final reconciliation",
        "",
        f'- Formations: **{len(combined["formations"])}**',
        f'- Plays: **{combined["total_plays"]}**',
        f'- Passed: **{combined["passed"]}**',
        f'- Failed: **{combined["failed"]}**',
        "",
    ]
    for item in combined["formations"]:
        lines.append(
            f'- **{item["formation"]}** — '
            f'{item["passed"]}/{item["total"]} passed'
        )
        if item["failed_plays"]:
            lines.append("  - Failed: " + ", ".join(item["failed_plays"]))
    (OUT / "nickel-final-reconciliation.md").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )

    if combined["failed"]:
        raise SystemExit(
            f'Nickel audit completed with {combined["failed"]} failed plays'
        )


if __name__ == "__main__":
    main()
