#!/usr/bin/env python3
"""Copy the two Simar skills to a supported local skill directory, without overwriting."""
from __future__ import annotations
import argparse
import json
import shutil
import tempfile
from pathlib import Path

NAMES = ("simar-canadian-immigration-intelligence", "simar-canadian-immigration-intelligence-monitor")
LEGACY_NAMES = ("simar-immigration-intelligence", "simar-immigration-monitor")
ROOT = Path(__file__).resolve().parent


def install(destination: Path, *, dry_run: bool = False) -> list[str]:
    destination = destination.expanduser().resolve()
    targets = [destination / name for name in NAMES]
    for name in LEGACY_NAMES:
        legacy = destination / name
        if legacy.exists() or legacy.is_symlink():
            raise FileExistsError(f"Previous Simar name detected: {legacy}. Back up and move this exact old skill folder before installing the renamed version; see INSTALL.md.")
    for name, target in zip(NAMES, targets):
        source = ROOT / "skills" / name
        if not (source / "SKILL.md").is_file():
            raise ValueError(f"Incomplete release: missing {name}/SKILL.md")
        if any(p.is_symlink() for p in source.rglob("*")):
            raise ValueError("Refusing a skill containing symbolic links")
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"Already exists: {target}. Keep it, or back it up and move that exact skill folder before updating.")
    if dry_run:
        return [str(p) for p in targets]
    destination.mkdir(parents=True, exist_ok=True)
    installed = []
    try:
        for name, target in zip(NAMES, targets):
            # Stage on the same filesystem. mkdir reserves the target without replacement.
            with tempfile.TemporaryDirectory(prefix=".simar-stage-", dir=destination) as temporary:
                stage = Path(temporary) / name
                shutil.copytree(ROOT / "skills" / name, stage)
                target.mkdir()
                installed.append(target)
                for child in stage.iterdir():
                    child.rename(target / child.name)
    except Exception:
        for path in installed:
            shutil.rmtree(path)
        raise
    return [str(p) for p in targets]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=["claude-code", "codex", "vscode", "generic"], required=True)
    parser.add_argument("--scope", choices=["user", "project"], default="user")
    parser.add_argument("--project", type=Path, default=Path.cwd())
    parser.add_argument("--destination", type=Path, help="Required for generic; exact skill parent folder")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.target == "generic":
        if args.destination is None:
            parser.error("generic requires --destination")
        destination = args.destination
    else:
        if args.destination is not None:
            parser.error("--destination is only for generic")
        if args.target == "vscode" and args.scope != "project":
            parser.error("Use --scope project for this VS Code installer")
        base = Path.home() if args.scope == "user" else args.project
        directory = {"claude-code": ".claude/skills", "codex": ".agents/skills", "vscode": ".github/skills"}[args.target]
        destination = base / directory
    try:
        paths = install(destination, dry_run=args.dry_run)
    except (OSError, ValueError) as exc:
        parser.exit(1, f"Not installed: {exc}\n")
    print(json.dumps({"status": "preview" if args.dry_run else "copied", "paths": paths,
                      "note": "Refresh the target host's skills list and test a prompt. No accounts, MCP connections or scheduled jobs were created."}, indent=2))


if __name__ == "__main__":
    main()
