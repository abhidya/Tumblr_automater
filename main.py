"""Offline-first Reddit-to-Tumblr automation archive.

The original project posted subreddit content to Tumblr accounts. This version
keeps the useful content-classification logic demoable without importing legacy
API clients or contacting Reddit/Tumblr by default.
"""

from __future__ import annotations

import argparse
import json
from configparser import RawConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".gif", ".webp")
VIDEO_HOSTS = ("youtube.com", "youtu.be", "vimeo.com")


@dataclass(frozen=True)
class Submission:
    title: str
    url: str
    selftext: str = ""


@dataclass(frozen=True)
class PlannedPost:
    post_type: str
    caption: str
    source: str


def classify_submission(submission: Submission, site_link: str = "") -> PlannedPost:
    """Return the Tumblr post payload that would be created for a submission."""
    title = submission.title
    clean_title = (
        title.replace("[Article]", "", 1)
        .replace("[Video]", "", 1)
        .replace("[Image]", "", 1)
        .strip()
    )
    caption = f"{clean_title} {site_link}".strip()
    lower_url = submission.url.lower()

    if any(host in lower_url for host in VIDEO_HOSTS) or "[video]" in title.lower():
        return PlannedPost("video", caption, submission.url)

    if lower_url.endswith(IMAGE_EXTENSIONS) or "[image]" in title.lower():
        return PlannedPost("photo", caption, submission.url)

    return PlannedPost("link", caption, submission.url)


def load_fixture(path: Path) -> list[Submission]:
    raw_items = json.loads(path.read_text(encoding="utf-8"))
    return [Submission(**item) for item in raw_items]


def load_accounts(path: Path) -> list[dict[str, str]]:
    parser = RawConfigParser()
    parser.read(path)
    return [{key: parser[section][key] for key in parser[section]} for section in parser.sections()]


def plan_posts(submissions: Iterable[Submission], site_link: str = "") -> list[PlannedPost]:
    return [classify_submission(submission, site_link) for submission in submissions]


def run_demo(args: argparse.Namespace) -> int:
    submissions = load_fixture(args.fixture)
    accounts = load_accounts(args.accounts)
    site_link = accounts[0].get("site_link", "") if accounts else ""
    planned = plan_posts(submissions, site_link)

    for index, post in enumerate(planned, start=1):
        print(f"{index}. {post.post_type}: {post.caption} -> {post.source}")

    print(f"planned_posts={len(planned)} dry_run=true")
    return 0


def run_live(_: argparse.Namespace) -> int:
    raise SystemExit(
        "Live posting is intentionally disabled in this archive. "
        "Rebuild it against current Reddit/Tumblr APIs with explicit rate limits first."
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Plan Reddit-to-Tumblr posts from an offline fixture.")
    parser.add_argument("--accounts", type=Path, default=Path("accounts.ini"))
    parser.add_argument("--fixture", type=Path, default=Path("fixtures/reddit_posts.json"))
    parser.add_argument("--live", action="store_true", help="Refuse live mode with an explicit safety message.")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    if args.live:
        return run_live(args)
    return run_demo(args)


if __name__ == "__main__":
    raise SystemExit(main())
