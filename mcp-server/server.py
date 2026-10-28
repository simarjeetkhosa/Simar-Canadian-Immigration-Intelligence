#!/usr/bin/env python3
"""Simar's read-only MCP workflow catalogue. MIT, Simarjeet Khosa, 2026."""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from mcp.types import ToolAnnotations

SUITE = Path(__file__).resolve().parents[1]
SKILLS = ("simar-canadian-immigration-intelligence", "simar-canadian-immigration-intelligence-monitor")
LIMITATION = (
    "Bundled workflow guidance, not current legal authority or a case database. "
    "Use the AI host's web tools to verify current primary sources and judgments. "
    "This server does not fill forms, control Adobe, schedule tasks, sign or submit. "
    "Form preparation requires a capable host and final human review."
)


def load_catalogue(root: Path = SUITE) -> dict[str, dict]:
    """Read only explicitly scoped, shipped Markdown. Never accept client paths."""
    root = root.resolve()
    candidates: list[Path] = []
    for name in SKILLS:
        folder = root / "skills" / name
        candidates.append(folder / "SKILL.md")
        candidates.extend(sorted((folder / "references").glob("*.md")))
    candidates.extend(sorted((root / "templates").glob("*.md")))
    catalogue = {}
    for path in candidates:
        relative = path.relative_to(root)
        if any(p.is_symlink() for p in [path, *path.parents] if p != root.parent):
            raise ValueError("Symlinks are not allowed in the public workflow catalogue")
        if not path.is_file() or not path.resolve().is_relative_to(root):
            raise ValueError(f"Missing or invalid bundled document: {relative}")
        raw = path.read_bytes()
        if len(raw) > 200_000:
            raise ValueError(f"Bundled document is too large: {relative}")
        content = raw.decode("utf-8")
        title = next((line[2:].strip() for line in content.splitlines() if line.startswith("# ")), path.stem)
        document_id = relative.with_suffix("").as_posix()
        catalogue[document_id] = {
            "document_id": document_id,
            "title": title,
            "sha256": hashlib.sha256(raw).hexdigest(),
            "content": content,
        }
    return catalogue


def build_server(*, host: str = "127.0.0.1", port: int = 8765,
                 allowed_hosts: list[str] | None = None,
                 allowed_origins: list[str] | None = None) -> FastMCP:
    catalogue = load_catalogue()
    mcp = FastMCP(
        "Simar Canadian Immigration Intelligence",
        instructions="Start with simar_list_workflows, retrieve the relevant documents, then apply them using host capabilities. " + LIMITATION,
        host=host, port=port, stateless_http=True, json_response=True,
        log_level="WARNING", max_request_body_size=65_536,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=allowed_hosts or ["127.0.0.1:*", "localhost:*", "[::1]:*"],
            allowed_origins=allowed_origins or ["http://127.0.0.1:*", "http://localhost:*"],
        ),
    )
    readonly = ToolAnnotations(readOnlyHint=True, destructiveHint=False,
                               idempotentHint=True, openWorldHint=False)

    @mcp.tool(annotations=readonly)
    def simar_list_workflows() -> dict[str, Any]:
        """List Simar's bundled immigration workflows and blank professional templates."""
        return {
            "documents": [{k: v for k, v in item.items() if k != "content"} for item in catalogue.values()],
            "limitations": LIMITATION,
            "current_law_verified": False,
        }

    @mcp.tool(annotations=readonly)
    def simar_get_document(document_id: str) -> dict[str, Any]:
        """Read a bundled workflow by exact ID returned by list/search. No file paths or case records."""
        if document_id not in catalogue:
            raise ValueError("Unknown document ID. Use simar_list_workflows; file paths are not accepted.")
        return {**catalogue[document_id], "limitations": LIMITATION, "current_law_verified": False}

    @mcp.tool(annotations=readonly)
    def simar_search_workflows(query: str, limit: int = 5) -> dict[str, Any]:
        """Search local workflow guidance by topic, such as JR, NOC, PNP or Adobe. Not a case-law/web search. Do not include client identifiers."""
        if not 1 <= limit <= 20:
            raise ValueError("limit must be between 1 and 20")
        if len(query) > 200:
            raise ValueError("Use a short topic query of at most 200 characters, without client data")
        terms = set(re.findall(r"[\w-]+", query.casefold()))
        if not terms:
            raise ValueError("Provide at least one topic word")
        matches = []
        for item in catalogue.values():
            haystack = (item["title"] + " " + item["content"]).casefold()
            score = sum(bool(re.search(r"(?<!\w)" + re.escape(term) + r"(?!\w)", haystack)) for term in terms)
            if score:
                matches.append({"document_id": item["document_id"], "title": item["title"], "matching_terms": score})
        matches.sort(key=lambda x: (-x["matching_terms"], x["document_id"]))
        return {"results": matches[:limit], "limitations": LIMITATION, "current_law_verified": False}

    @mcp.resource("simar://about")
    def about() -> str:
        return "Simar Canadian Immigration Intelligence 1.0.1. Copyright (c) 2026 Simarjeet Khosa. MIT License.\n" + LIMITATION

    @mcp.prompt()
    def prepare_case_audit() -> str:
        """Start an immigration case audit with evidence, source and human-review checks."""
        return (
            "Use simar_get_document for skills/simar-canadian-immigration-intelligence/SKILL, "
            "skills/simar-canadian-immigration-intelligence/references/professional-use-and-portability "
            "and templates/CASE_AUDIT. Ask only for material missing facts. "
            "Check urgent dates before broader research, retrieve current primary sources, "
            "separate evidence from assumptions and prepare a draft for the appropriate human reviewer. "
            "For JR also retrieve references/jr-case-audit under the same skill."
        )

    return mcp


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--allowed-host", action="append", help="Exact trusted Host header, repeat as needed (e.g. mcp.your-firm.example)")
    parser.add_argument("--allowed-origin", action="append", help="Explicit trusted Origin, repeat as needed")
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("port must be between 1 and 65535")
    if args.host not in {"127.0.0.1", "localhost", "::1"} and not args.allowed_host:
        parser.error("A non-loopback listener requires an explicit --allowed-host")
    if any("*" in value for value in (args.allowed_host or []) + (args.allowed_origin or [])):
        parser.error("Wildcard-all hosts/origins are not allowed; specify trusted values")
    mcp = build_server(host=args.host, port=args.port,
                       allowed_hosts=args.allowed_host, allowed_origins=args.allowed_origin)
    mcp.run(transport=args.transport)


if __name__ == "__main__":
    main()
