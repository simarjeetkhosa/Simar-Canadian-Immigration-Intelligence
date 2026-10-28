"""Integration checks for actual MCP transports and safe local installation."""
from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import socket
import subprocess
import sys
import time
import tomllib
from pathlib import Path

import httpx
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.streamable_http import streamable_http_client

ROOT = Path(__file__).resolve().parents[1]
SERVER = ROOT / "mcp-server/server.py"


async def check_tools(session):
    initialized = await session.initialize()
    assert initialized.serverInfo.name == "Simar Canadian Immigration Intelligence"
    listed = await session.list_tools()
    assert {t.name for t in listed.tools} == {
        "simar_list_workflows", "simar_get_document", "simar_search_workflows"
    }
    assert all(t.annotations.readOnlyHint and not t.annotations.openWorldHint for t in listed.tools)
    catalogue = await session.call_tool("simar_list_workflows")
    documents = catalogue.structuredContent["documents"]
    assert len(documents) >= 20
    assert catalogue.structuredContent["current_law_verified"] is False
    searched = await session.call_tool("simar_search_workflows", {"query": "judicial", "limit": 20})
    assert any("jr-case-audit" in r["document_id"] for r in searched.structuredContent["results"])
    document = await session.call_tool("simar_get_document", {"document_id": "templates/HUMAN_REVIEW"})
    assert "Human review completed: **No**" in document.structuredContent["content"]
    assert document.structuredContent["current_law_verified"] is False
    for bad in ("../../LICENSE", str(Path.home() / "private.txt"), "not-found"):
        result = await session.call_tool("simar_get_document", {"document_id": bad})
        assert result.isError
    for args in ({"query": " "}, {"query": "x" * 201}, {"query": "PNP", "limit": 0}):
        assert (await session.call_tool("simar_search_workflows", args)).isError
    empty = await session.call_tool("simar_search_workflows", {"query": "zzznomatchzzzz"})
    assert empty.structuredContent["results"] == []
    about = await session.read_resource("simar://about")
    assert "Simarjeet Khosa" in about.contents[0].text
    assert (await session.get_prompt("prepare_case_audit")).messages


def test_real_stdio_protocol():
    async def run():
        parameters = StdioServerParameters(command=sys.executable, args=[str(SERVER)])
        async with stdio_client(parameters) as (read, write):
            async with ClientSession(read, write) as session:
                await check_tools(session)
    asyncio.run(run())


def test_real_http_protocol_and_untrusted_host():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
    process = subprocess.Popen([sys.executable, str(SERVER), "--transport", "streamable-http", "--port", str(port)],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    url = f"http://127.0.0.1:{port}/mcp"
    try:
        for _ in range(100):
            if process.poll() is not None:
                raise AssertionError("HTTP server exited before becoming ready")
            try:
                response = httpx.get(url, timeout=0.2, trust_env=False)
                break
            except httpx.ConnectError:
                time.sleep(0.05)
        else:
            raise AssertionError("HTTP server did not become ready")
        hostile = httpx.get(url, headers={"host": "untrusted.example"}, timeout=2, trust_env=False)
        assert hostile.status_code in {400, 403, 421}

        async def run():
            async with httpx.AsyncClient(trust_env=False, timeout=10) as http_client:
                async with streamable_http_client(url, http_client=http_client) as (read, write, _):
                    async with ClientSession(read, write) as session:
                        await check_tools(session)
        asyncio.run(run())
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def test_installer_preview_copy_and_preserve_existing(tmp_path):
    destination = tmp_path / "skills"
    command = [sys.executable, str(ROOT / "install.py"), "--target", "generic", "--destination", str(destination)]
    preview = subprocess.run(command + ["--dry-run"], check=True, capture_output=True, text=True)
    assert json.loads(preview.stdout)["status"] == "preview"
    assert not destination.exists()
    subprocess.run(command, check=True, capture_output=True)
    installed = destination / "simar-canadian-immigration-intelligence/SKILL.md"
    original = installed.read_bytes()
    sentinel = destination / "unrelated.txt"
    sentinel.write_text("keep me")
    again = subprocess.run(command, capture_output=True, text=True)
    assert again.returncode != 0 and "Already exists" in again.stderr
    assert installed.read_bytes() == original
    assert sentinel.read_text() == "keep me"
    assert (destination / "simar-canadian-immigration-intelligence-monitor/LICENSE").is_file()
    legacy_destination = tmp_path / "legacy-skills"
    legacy_folder = legacy_destination / "simar-immigration-intelligence"
    legacy_folder.mkdir(parents=True)
    legacy_file = legacy_folder / "SKILL.md"
    legacy_file.write_text("existing user's version")
    legacy_attempt = subprocess.run(
        [sys.executable, str(ROOT / "install.py"), "--target", "generic", "--destination", str(legacy_destination)],
        capture_output=True, text=True)
    assert legacy_attempt.returncode != 0 and "Previous Simar name detected" in legacy_attempt.stderr
    assert legacy_file.read_text() == "existing user's version"
    assert not (legacy_destination / "simar-canadian-immigration-intelligence").exists()


def test_generated_config_and_refuse_overwrite(tmp_path):
    command = [sys.executable, str(ROOT / "configure_mcp.py"), "--python", sys.executable,
               "--output-dir", str(tmp_path)]
    subprocess.run(command, check=True, capture_output=True)
    claude = json.loads((tmp_path / "claude-desktop.json").read_text())["mcpServers"]["simar-canadian-immigration-intelligence"]
    codex = tomllib.loads((tmp_path / "codex-config.toml").read_text())["mcp_servers"]["simar-canadian-immigration-intelligence"]
    vscode = json.loads((tmp_path / "vscode-mcp.json").read_text())["servers"]["simar-canadian-immigration-intelligence"]
    assert claude["command"] == str(Path(sys.executable).absolute()) == codex["command"] == vscode["command"]
    assert claude["args"] == codex["args"] == vscode["args"] == [str(SERVER)]
    assert subprocess.run(command, capture_output=True).returncode != 0


def test_server_rejects_unscoped_bind():
    result = subprocess.run([sys.executable, str(SERVER), "--transport", "streamable-http", "--host", "0.0.0.0"],
                            capture_output=True, text=True, timeout=10)
    assert result.returncode != 0 and "--allowed-host" in result.stderr
