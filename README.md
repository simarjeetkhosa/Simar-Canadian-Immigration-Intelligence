# Simar Canadian Immigration Intelligence

**AI agent skills for Canadian immigration research, case preparation, drafting and human review.**

Created by **Simarjeet Khosa** · Version 1.0.1 · MIT License

[Download release ZIP](releases/Simar-Canadian-Immigration-Intelligence-v1.0.1.zip) · [Detailed installation](INSTALL.md) · [Validation](VALIDATION.md) · [License](LICENSE)

## Use, share and contribute

**You are welcome to use these skills, adapt them for your work, and share improvements.** The [MIT License](LICENSE) permits personal and commercial use, modification and redistribution when its copyright and license notice are preserved. AI services and third-party materials retain their own terms.

[Get installation help](SUPPORT.md) · [Report a bug](https://github.com/simarjeetkhosa/Simar-Canadian-Immigration/issues/new?template=bug.yml) · [Suggest an improvement](https://github.com/simarjeetkhosa/Simar-Canadian-Immigration/issues/new?template=feature.yml) · [Contribute a change](CONTRIBUTING.md)

New to GitHub? Use the help link to describe your setup, or fork this repository and submit a pull request for an improvement. Contributions are reviewed before merging. Use fictional examples in community posts.

## About the skills

A skill is a reusable set of instructions, reference material and optional scripts that an AI agent loads for a specific task. Your chosen AI application provides the model, research tools, file execution and connected services.

| Skill | What it helps with |
| --- | --- |
| **Simar Canadian Immigration Intelligence** | Program screening, Express Entry, provincial pathways, AAIP, RCIP/FCIP, work permits, NOC/TEER comparisons, evidence checklists, English/Punjabi drafts, submission letters, refusal and judicial-review issue audits, and source verification. |
| **Simar Canadian Immigration Intelligence Monitor** | Requested immigration digests, policy/intake watches and reminders. Recurring runs require a separate supported scheduler and an explicit schedule request. |

The package also includes blank case-audit and human-review templates, optional PDF helpers, and a read-only MCP workflow server. Results depend on the AI host's actual capabilities. The suite supports professional preparation and review; final advice, filings and form approval remain with the responsible human reviewer.

## Upgrading from v1.0.0

The skill folders are now named `simar-canadian-immigration-intelligence` and `simar-canadian-immigration-intelligence-monitor`. Back up and move the previous `simar-immigration-intelligence` and `simar-immigration-monitor` folders out of your host's skill directory before installing. For uploaded skills, disable/remove the earlier copies before enabling the renamed ones. The installer detects legacy names and stops to prevent duplicates. See [migration details](INSTALL.md).

## Start here

1. Download the release ZIP above, or choose **Code → Download ZIP** for the latest repository files.
2. Extract it. Open the folder containing `install.py`, `skills/` and `uploads/`.
3. Choose your AI below. Install both skills once per host, then verify they appear in its skills list.
4. Try the example request near the bottom of this page.

Because this repository is private, downloads and cloning require an authorized GitHub account. Platform versions and workspace policies may affect availability.

## Choose your AI

| AI application | Installation route |
| --- | --- |
| Claude web / desktop with custom skills | Upload the two individual skill ZIPs. |
| Claude Code | Run the bundled installer for `claude-code`. |
| ChatGPT desktop with personal skills | Use its Skill Creator with the two individual skill ZIPs. |
| Codex CLI / IDE | Run the bundled installer for `codex`. |
| Gemini CLI | Install each local skill folder using Gemini's own skill command. |
| Gemini web / Gems or another chat assistant | Use the instruction/knowledge fallback if file context and custom instructions are supported. |
| VS Code / GitHub Copilot with Agent Skills | Install into the project's `.github/skills` directory. |
| Cursor, Windsurf, Cline, Roo Code, Antigravity and other agents | Use the host's documented Agent Skills importer or directory; otherwise use MCP or the context fallback below. Support varies by product and version. |

### Claude web and desktop

In **Customize → Skills**, choose **+ → Create skill → Upload a skill**. Upload these separately and enable both:

- [`simar-canadian-immigration-intelligence.zip`](uploads/simar-canadian-immigration-intelligence.zip)
- [`simar-canadian-immigration-intelligence-monitor.zip`](uploads/simar-canadian-immigration-intelligence-monitor.zip)

Enable code execution/file creation as required by your account. Upload the individual skill ZIPs, rather than the whole suite. See [Claude's official instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

### Claude Code

Requires Python 3.10+. Run from the extracted suite folder:

```sh
python3 install.py --target claude-code --scope user --dry-run
python3 install.py --target claude-code --scope user
```

This copies both skills into `~/.claude/skills/`. Start a fresh session and ask Claude to use Simar Canadian Immigration Intelligence. [Official Claude Code guide](https://code.claude.com/docs/en/skills).

### ChatGPT desktop

Where personal skills and Skill Creator are available, attach the two individual ZIPs from `uploads/` and ask:

> Use Skill Creator to install Simar Canadian Immigration Intelligence and Simar Canadian Immigration Intelligence Monitor from these ZIPs. Preserve their references and scripts. Do not create scheduled tasks.

Confirm both appear in **Skills**, then select a skill with `@`. Attaching files alone does not prove installation. This repository is a standalone skills package; it is not a published ChatGPT marketplace plugin. See [OpenAI's skills guide](https://learn.chatgpt.com/docs/build-skills).

### Codex CLI and IDE

From the extracted suite folder:

```sh
python3 install.py --target codex --scope user --dry-run
python3 install.py --target codex --scope user
```

The bundled installer copies both folders into `~/.agents/skills/`. Refresh or restart if they do not appear. Invoke `$simar-canadian-immigration-intelligence` or `$simar-canadian-immigration-intelligence-monitor`. To install for one project, replace `--scope user` with `--scope project --project "/path/to/project"`.

### Gemini CLI

With Gemini CLI already installed, run from the extracted suite folder:

```sh
gemini skills install ./skills/simar-canadian-immigration-intelligence
gemini skills install ./skills/simar-canadian-immigration-intelligence-monitor
gemini skills list --all
```

Review Gemini's installation prompts. In an interactive session, use `/skills reload` and `/skills list`, then ask it to use the selected Simar skill. These are Gemini CLI commands; the bundled Python installer has no `gemini` target. See [Google's official Agent Skills guide](https://geminicli.com/docs/cli/skills/).

### VS Code / GitHub Copilot

For a VS Code agent with Agent Skills enabled:

```sh
python3 install.py --target vscode --scope project --project "/path/to/project" --dry-run
python3 install.py --target vscode --scope project --project "/path/to/project"
```

This writes the two skill folders under the project's `.github/skills/`. Open that project in VS Code and confirm discovery. See [Microsoft's Agent Skills guide](https://code.visualstudio.com/docs/agent-customization/agent-skills).

### Other AI agents with native skills

Use the application's documented skill import flow with each folder under `skills/`. Preserve `SKILL.md`, references, scripts, assets and licensing together. If the host documents a compatible local directory, the generic installer can copy both skills there:

```sh
python3 install.py --target generic --destination "/absolute/path/to/host/skills" --dry-run
python3 install.py --target generic --destination "/absolute/path/to/host/skills"
```

Replace the example destination with the actual documented directory. Copying files does not establish compatibility; confirm the host discovers both skills and loads their references. Use one installation route per host to avoid duplicates.

### Gemini web, Gems and assistants without a skill loader

If your application supports custom instructions and reference files:

1. Add [`adapters/host-instructions.txt`](adapters/host-instructions.txt) to its custom instructions.
2. Add [`adapters/simar-canadian-immigration-intelligence-knowledge.md`](adapters/simar-canadian-immigration-intelligence-knowledge.md) as reference knowledge or file context, subject to the host's file limits.
3. Ask it to use the Simar workflow and confirm which files it can read.

This gives the assistant workflow context. It does not install native skills, run the Python helpers, enable live research or create an autonomous agent. If uploads are unavailable, provide the relevant reference section in the conversation.

## Optional: connect an MCP-capable agent

The included MCP server exposes bundled workflow documents and blank templates through three read-only tools: `simar_list_workflows`, `simar_get_document` and `simar_search_workflows`.

On macOS/Linux, from the suite folder:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r mcp-server/requirements.txt
.venv/bin/python configure_mcp.py --python .venv/bin/python
```

Use the generated `local-config/` snippets in your client's documented MCP settings. Keep the suite folder in place. The [detailed guide](INSTALL.md#4-start-the-mcp-server-locally) covers Windows, stdio, HTTP and remote hosting. A cloud AI cannot reach your Mac's loopback address directly. No hosted endpoint is included.

## Try your first request

> Use Simar Canadian Immigration Intelligence to prepare a blank Canadian immigration case-audit checklist. Separate confirmed facts, missing evidence, research questions and human-review steps. Do not invent client facts.

Other examples:

- “Compare these confirmed job duties with current NOC descriptions and cite the primary sources.”
- “Audit this refusal and build an evidence-linked issue matrix for counsel review.”
- “Draft an English and Punjabi client document checklist from these confirmed facts.”
- “Use Simar Canadian Immigration Intelligence Monitor to prepare a one-time update on these specified programs.”

For recurring monitoring, separately confirm the topics, frequency, timezone and destination in a host with a scheduler.

## Verify installation and troubleshoot

- **Skills missing:** confirm both named folders contain `SKILL.md`; refresh the host or start a new session.
- **Installer says already exists:** back up and move only the exact old Simar folders before reinstalling; it deliberately avoids overwriting.
- **No live sources or file tools:** connect the capabilities through the host. Installing instructions does not grant tool access.
- **Forms:** PDF helpers are optional; see [PDF setup](INSTALL.md#6-enable-pdf-and-adobe-workflows). Drafts require review, and specialized XFA/barcode forms need an appropriate validation workflow.
- **Remove:** use the host's skill uninstall flow, or remove only the two installed Simar folders. Disconnect MCP separately if configured.

Installation is confirmed when both skills are discoverable and the host can produce the blank audit checklist using the correct references. Platform instructions were checked against the linked vendor documentation on 28 October 2026; end-to-end installation has not been tested in every AI application.

## Package and license

[`skills/`](skills/) · [`uploads/`](uploads/) · [`templates/`](templates/) · [`mcp-server/`](mcp-server/) · [Detailed installation](INSTALL.md) · [Test scope](VALIDATION.md)

Copyright (c) 2026 Simarjeet Khosa. Distributed under the [MIT License](LICENSE); preserve [NOTICE.md](NOTICE.md) when redistributing. The v1.0.1 ZIP is the supplied release archive. Its checksums describe the packaged release; this repository's main guide includes community documentation updates.
