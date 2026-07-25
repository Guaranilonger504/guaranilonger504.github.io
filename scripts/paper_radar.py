#!/usr/bin/env python3
from __future__ import annotations

import argparse
import logging
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

from openai import OpenAI

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from paper_radar.core import fetch_arxiv, load_config, parse_atom, run_pipeline


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Generate the Shiori Route paper radar")
    result.add_argument("--config", default="config/paper-radar.yaml")
    result.add_argument("--date", help="Run date in YYYY-MM-DD (UTC); defaults to now")
    result.add_argument("--fixture", help="Read an arXiv Atom fixture instead of the network")
    mode = result.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="Fetch and plan only; no OpenAI and no writes")
    mode.add_argument("--fetch-only", action="store_true", help="Fetch and report only; no OpenAI and no writes")
    mode.add_argument("--analyze", action="store_true", help="Explicitly run analysis (default mode)")
    return result


def main() -> int:
    args = parser().parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    root = ROOT
    config = load_config(root / args.config)
    now = datetime.fromisoformat(args.date).replace(tzinfo=UTC) if args.date else datetime.now(UTC)
    papers = (
        parse_atom((root / args.fixture).read_text(encoding="utf-8"))
        if args.fixture
        else fetch_arxiv(config, now)
    )
    client = None
    if not (args.dry_run or args.fetch_only):
        api_key = os.environ.get("OPENAI_API_KEY")
        if api_key:
            client = OpenAI(api_key=api_key, timeout=config["limits"]["timeout_seconds"], max_retries=0)
    try:
        result = run_pipeline(
            root,
            config,
            now=now,
            papers=papers,
            client=client,
            dry_run=args.dry_run,
            fetch_only=args.fetch_only,
        )
    except Exception:
        logging.exception("Paper radar failed")
        return 1
    logging.info(
        "Done: fetched=%d new=%d screened=%d recommended=%d deep=%d failed=%d changed=%s",
        result.fetched, result.new, result.screened, result.recommended,
        result.deep, result.failed, result.changed,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
