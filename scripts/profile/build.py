"""Render assets/profile.svg: the minimal card on even days, the terminal card on odd days.

Projects are the owner's repos sorted by most recent push. With PROFILE_TOKEN set (a
token that can read private repo metadata) private repos are included; otherwise only
public ones, read with GITHUB_TOKEN when available.

    python scripts/profile/build.py [--style minimal|terminal] [--out PATH]
"""
import argparse
import datetime
import json
import os
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import minimal  # noqa: E402
import terminal  # noqa: E402

USER = "jerryinyang"
STYLES = {"minimal": minimal, "terminal": terminal}
ROOT = Path(__file__).resolve().parents[2]


def fetch_repos():
    private_token = os.environ.get("PROFILE_TOKEN")
    token = private_token or os.environ.get("GITHUB_TOKEN")
    if private_token:
        base = "https://api.github.com/user/repos?affiliation=owner&visibility=all"
    else:
        base = f"https://api.github.com/users/{USER}/repos?type=owner"
    repos, page = [], 1
    while True:
        req = urllib.request.Request(f"{base}&sort=pushed&per_page=100&page={page}",
                                     headers={"Accept": "application/vnd.github+json"})
        if token:
            req.add_header("Authorization", f"Bearer {token}")
        with urllib.request.urlopen(req, timeout=30) as resp:
            batch = json.load(resp)
        repos += batch
        if len(batch) < 100:
            return repos
        page += 1


def recent_projects(repos):
    keep = [r for r in repos
            if not r["fork"] and not r["archived"] and r["name"].lower() != USER]
    keep.sort(key=lambda r: r["pushed_at"] or "", reverse=True)
    return [r["name"] for r in keep]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--style", choices=STYLES)
    ap.add_argument("--out", type=Path, default=ROOT / "assets" / "profile.svg")
    args = ap.parse_args()

    today = datetime.datetime.now(datetime.timezone.utc).date()
    style = args.style or ("minimal" if today.toordinal() % 2 == 0 else "terminal")
    repos = fetch_repos()
    if os.environ.get("PROFILE_TOKEN") and not any(r["private"] for r in repos):
        print("warning: PROFILE_TOKEN is set but sees no private repos; "
              "give it access to all repositories, not public ones only", file=sys.stderr)
    projects = recent_projects(repos)
    svg = STYLES[style].render(projects)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(svg)
    print(f"{style}: {len(svg) / 1024:.1f} KB, projects: {', '.join(projects[:7])}")


if __name__ == "__main__":
    main()
