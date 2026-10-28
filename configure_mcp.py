#!/usr/bin/env python3
"""Generate local MCP connection snippets. Does not edit any AI application's settings."""
import argparse
import json
from pathlib import Path


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--python", required=True, type=Path, help="Python executable in the venv where MCP requirements were installed")
    p.add_argument("--output-dir", type=Path, default=Path("local-config"))
    args = p.parse_args()
    # Preserve a venv executable symlink: resolving it would run the base interpreter.
    executable = args.python.expanduser().absolute()
    if not executable.is_file():
        p.error("Python executable does not exist")
    script = Path(__file__).resolve().parent / "mcp-server/server.py"
    command = {"command": str(executable), "args": [str(script)]}
    outputs = {
        "claude-desktop.json": json.dumps({"mcpServers": {"simar-immigration": command}}, indent=2),
        "vscode-mcp.json": json.dumps({"servers": {"simar-immigration": {"type": "stdio", **command}}}, indent=2),
        "codex-config.toml": "[mcp_servers.simar-immigration]\ncommand = " + json.dumps(str(executable)) + "\nargs = [" + json.dumps(str(script)) + "]\n",
    }
    destination = args.output_dir.expanduser().absolute()
    if any((destination / name).exists() for name in outputs):
        p.error("Config output exists; use a new output directory")
    destination.mkdir(parents=True, exist_ok=True)
    for name, content in outputs.items():
        with (destination / name).open("x", encoding="utf-8") as f:
            f.write(content + "\n")
    print(f"Created connection snippets in {destination}. Merge the relevant entry; do not replace unrelated server settings.")


if __name__ == "__main__":
    main()
