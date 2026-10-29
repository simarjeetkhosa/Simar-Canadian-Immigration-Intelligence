# Install Simar Canadian Immigration Intelligence

Version 1.0.3 • 29 October 2026 • Copyright (c) 2026 Simarjeet Khosa • MIT License

Start by extracting this entire release ZIP. Keep the extracted folder in a permanent location if you use its MCP server. Choose one skill installation method per AI host to avoid duplicate copies. Installing a skill does not connect Adobe, enable web access, create schedules or submit cases.

## Choose an option

| Your AI environment | Recommended option | What you receive |
| --- | --- | --- |
| Claude with custom skills | Upload the two ZIPs inside `uploads/`, one at a time | Native skill instructions, references and optional scripts |
| ChatGPT with personal skills | Use Skill Creator to install the two supplied skill ZIPs | Personal skills, subject to the account's capabilities |
| Codex CLI / IDE | Run the local installer for `codex` | Native skills under `.agents/skills` |
| Claude Code | Run the local installer for `claude-code` | Native skills under `.claude/skills` |
| VS Code agent supporting skills | Run the project installer for `vscode` | Skills under `.github/skills` |
| Other AI with an MCP client | Start the MCP server and configure the supported transport | Searchable workflow guidance and blank review templates |
| AI with file context but no skill loader | Load `adapters/host-instructions.txt` and `adapters/simar-canadian-immigration-intelligence-knowledge.md` | Instruction/knowledge fallback; no tools are installed |

Availability depends on the host version, plan and organizational policy. The code is locally tested; this release has not been installed or tested inside your Claude account or every listed AI product.

## Updating an earlier Simar installation

The main name is now **Simar Canadian Immigration Intelligence**, and the companion is **Simar Canadian Immigration Intelligence Monitor**. Their folder names are `simar-canadian-immigration-intelligence` and `simar-canadian-immigration-intelligence-monitor`.

For a local v1.0.0 installation, back up and move only the previous `simar-immigration-intelligence` and `simar-immigration-monitor` folders out of the host's active skill directory before installing these renamed folders. The installer detects the old names and stops to avoid duplicate skills. For an uploaded skill in another AI account, use that host's supported replacement or removal flow to avoid keeping both names active. Your personal skills in the originating ChatGPT account were renamed in place.

If MCP was already configured, generate fresh snippets pointing at the renamed release folder. Update the old Simar entry to the new connection name rather than leaving two connections enabled. The public MCP tool names and `simar://about` resource remain stable; workflow document IDs now use the renamed skill folders, so retrieve current IDs with `simar_list_workflows`.

## 1. Upload to Claude

Open **Customize → Skills**, select **+ → Create skill → Upload a skill**, and upload `uploads/simar-canadian-immigration-intelligence.zip`. Repeat with `uploads/simar-canadian-immigration-intelligence-monitor.zip`. Ensure the account permits custom skills and code execution. Do not upload the entire release ZIP as one skill.

Each upload ZIP has one named skill folder containing `SKILL.md`, its referenced files, and `LICENSE`. Keep that structure. Enable the skills and test: “Use Simar Canadian Immigration Intelligence to prepare a case-audit template, without inventing client facts.”

See [Claude's official skill instructions](https://support.claude.com/en/articles/12512180-use-skills-in-claude). A successful file attachment in a chat is not evidence that a skill was installed.

## 2. Install in ChatGPT

Your personal Simar skills have been updated in the originating ChatGPT account. To install in another supported account, attach the two individual skill ZIPs and ask:

> Use Skill Creator to install Simar Canadian Immigration Intelligence and Simar Canadian Immigration Intelligence Monitor from these ZIPs. Keep their supporting references and scripts. Do not create any scheduled tasks.

Confirm both skills appear in that account's Skills list. Invoke Simar explicitly using the available skill selector. If the account does not provide a skill installation feature, use the instruction/knowledge fallback or an MCP connection below; a plain attachment does not add execution permissions.

OpenAI distinguishes local/standalone skills from plugin distribution. See [Build skills](https://learn.chatgpt.com/docs/build-skills) and [Skills and plugins](https://learn.chatgpt.com/docs/skills-and-plugins). This release is not a published marketplace plugin.

## 3. Install into a local agent

Requires Python 3.10 or later. Open a terminal in the extracted release folder. Use `python3` on macOS/Linux or `py -3` on Windows where appropriate.

Preview, then install for Claude Code:

```sh
python3 install.py --target claude-code --scope user --dry-run
python3 install.py --target claude-code --scope user
```

For Codex CLI/IDE:

```sh
python3 install.py --target codex --scope user --dry-run
python3 install.py --target codex --scope user
```

For a project, supply its folder explicitly:

```sh
python3 install.py --target vscode --scope project --project "/path/to/your/project" --dry-run
python3 install.py --target vscode --scope project --project "/path/to/your/project"
```

The `claude-code` and `codex` targets also accept `--scope project --project ...`. The installer refuses to replace either existing Simar folder. To update, keep a backup and move only the existing named Simar folders out of the target skill directory, then rerun. To remove this local installation, remove only those two installed folders. Do not delete the parent skills directory.

For another host that documents a compatible skill directory:

```sh
python3 install.py --target generic --destination "/path/to/host/skills" --dry-run
python3 install.py --target generic --destination "/path/to/host/skills"
```

The generic option only copies files. It does not certify that an arbitrary AI supports Agent Skills. Refresh the host's skills list and confirm a test prompt loads the correct instructions.

Official directory references: [Claude Code skills](https://code.claude.com/docs/en/skills), [Codex skill locations](https://learn.chatgpt.com/docs/build-skills), [VS Code skills](https://code.visualstudio.com/docs/agent-customization/agent-skills).

## 4. Start the MCP server locally

The server offers three read-only tools: `simar_list_workflows`, `simar_get_document`, and `simar_search_workflows`. It also supplies a case-audit prompt and an about resource. It reads only bundled workflow documents and blank templates. It has no browser, client-file access tool, form-filling endpoint, Adobe control, scheduler or filing endpoint.

Create an isolated Python environment and install the official MCP SDK:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r mcp-server/requirements.txt
.venv/bin/python configure_mcp.py --python .venv/bin/python
```

On Windows PowerShell:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r mcp-server/requirements.txt
.\.venv\Scripts\python.exe configure_mcp.py --python .\.venv\Scripts\python.exe
```

`local-config/` now contains connection snippets with the actual absolute paths on your computer. The generator does not modify an AI application's settings. Keep the venv and extracted release in place while the server is configured.

| MCP client | Configure |
| --- | --- |
| Claude Desktop with local MCP support | Merge the `mcpServers` entry from `local-config/claude-desktop.json` into its documented local MCP configuration. Preserve other servers. |
| Claude Code | Use its documented MCP configuration/add flow with the same Python command and server.py argument. |
| Codex | Merge `local-config/codex-config.toml` into the host's MCP settings, or use `codex mcp add simar-canadian-immigration-intelligence -- /absolute/path/to/venv/python /absolute/path/to/mcp-server/server.py`. |
| ChatGPT desktop with local MCP support | In Settings → MCP servers, add a STDIO server using the generated Python command and server.py argument. Follow the current host's connection refresh flow. |
| VS Code | Use its MCP add flow, or merge `local-config/vscode-mcp.json` into `.vscode/mcp.json` for the supported compatibility configuration. Its `servers` schema differs from the portable `mcpServers` schema. |
| Another stdio MCP client | Use the venv Python executable as the command and the absolute path to server.py as its argument. |

No API key is required by this read-only server. The AI host itself may require an account or subscription. Start with: “List Simar workflows, then retrieve the JR audit and human-review template.” Verify that all three tools are discoverable and a document can be retrieved. Typing server.py directly starts a waiting stdio process; silence in the terminal is normal because the MCP client communicates over stdin/stdout.

See the official [MCP Python SDK v1 documentation](https://py.sdk.modelcontextprotocol.io/v1/), [Claude Code MCP guide](https://code.claude.com/docs/en/mcp), [OpenAI MCP guide](https://learn.chatgpt.com/docs/extend/mcp), and [VS Code MCP guide](https://code.visualstudio.com/docs/agent-customization/mcp-servers).

## 5. Connect through remote MCP, including ChatGPT web

For local HTTP testing:

```sh
.venv/bin/python mcp-server/server.py --transport streamable-http --port 8765
```

The local endpoint is `http://127.0.0.1:8765/mcp`. This address is not reachable from an unrelated cloud AI account. ChatGPT web supports a reachable HTTPS MCP endpoint or a supported Secure MCP Tunnel; it does not read your local Codex settings.

For public hosting, an administrator can run this same read-only catalogue behind a trusted HTTPS reverse proxy. Example application command, replacing the example hostname:

```sh
.venv/bin/python mcp-server/server.py --transport streamable-http --host 0.0.0.0 --port 8765 --allowed-host mcp.your-firm.example
```

Keep the upstream port private, forward the expected Host header, and route `/mcp` without buffering streamed responses. If a legitimate client sends an Origin header, allow its exact trusted origin with `--allowed-origin`. DNS-rebinding protection remains enabled. Do not disable it to fix a configuration error. Configure the proxy to avoid logging MCP request bodies and apply appropriate request limits.

This public configuration exposes only the distributed workflow text and blank templates; it supplies no authentication implementation. Do not put firm-private documents or client records into the served skill/reference/template folders. Adding private services requires a separately designed authorization and data-isolation layer. A tunnel can keep the service private where supported.

In ChatGPT's current custom-MCP flow, open Plugins, choose **+ → Add custom MCP server**, enter the HTTPS `/mcp` URL or select a supported tunnel, configure the authentication that the actual service provides, create the connection, and inspect its tools. Follow account/workspace controls. Use [OpenAI's connection guide](https://developers.openai.com/plugins/deploy/connect-chatgpt) and [Secure MCP Tunnel documentation](https://developers.openai.com/api/docs/guides/secure-mcp-tunnels).

**No remote service, domain, tunnel or external AI account connection has been created by this release.** Public plugin submission is a separate process. For other remote MCP clients, use their current supported HTTP connection workflow and the same deployed `/mcp` endpoint.

## 6. Enable PDF and Adobe workflows

The skill contains local helpers for standard PDF form drafts and document assembly. In an environment with Python execution, install their optional dependencies:

```sh
.venv/bin/python -m pip install -r pdf-requirements.txt
.venv/bin/python skills/simar-canadian-immigration-intelligence/scripts/fill_pdf_form.py inspect "/path/to/form.pdf"
```

After reviewing the field inventory, create `confirmed-fields.json` mapping exact field names to confirmed values. Then:

```sh
.venv/bin/python skills/simar-canadian-immigration-intelligence/scripts/fill_pdf_form.py fill "/path/to/form.pdf" --values "/path/to/confirmed-fields.json" --output "/path/to/draft.pdf" --report "/path/to/review.json"
```

Unknown or unsupported field types fail rather than being guessed. The draft and review manifest require human review. XFA, calculations, barcode and signed/encrypted forms need the specialized route described in the skill. Never flatten or regenerate a barcode form to bypass its validation. Optional OCR/compression requires separately installed system tools such as OCRmyPDF/Tesseract or Ghostscript; consult the document-assembly reference before use.

Where Adobe Acrobat is connected, let the agent discover its actual operations. The current connected tool set includes editing interfaces, OCR, extraction, conversion, compression and page organization. It does not establish unattended filling or XFA/barcode validation. Use a capable application for those requirements and record what was actually validated. Copying this package does not install or transfer an Adobe connection or licence.

## 7. Configure professional use

Complete `templates/FIRM_PROFILE.json` privately with the responsible professional, jurisdiction, timezone and approved data-handling preferences. It is a configuration worksheet; no component automatically loads it. Supply the relevant settings to your AI host or firm instructions. Do not put client credentials in it or add it to a public server catalogue.

Use `templates/CASE_AUDIT.md` and `templates/HUMAN_REVIEW.md` as reusable blank work products. The skills support all-PNP/AAIP/RCIP research, Express Entry and non-Express Entry pathways, work permits, NOC matching, natural submission letters, refusal/JR audit and verified case-law integration. Each actual case still needs current primary sources and its own evidence.

Choose a responsible human reviewer. Do not infer that a role permits representation in every forum. The [Federal Court's representation guidance](https://www.fct-cf.ca/en/pages/who-may-represent-you-in-an-immigration-refugee-protection-or-citizenship-matter-in-federal-court) and [IRCC authorization guidance](https://www.canada.ca/en/immigration-refugees-citizenship/services/immigration-citizenship-representative/choose/authorized.html) are starting points for current checks. MIT is a software licence, not a professional credential.

For recurring monitoring, explicitly request a schedule in a host with a supported scheduler and research access. Confirm the saved task, timezone, scope and destination. Neither the skill upload nor this MCP server starts a daily job.

## Troubleshooting and acceptance check

- Skill missing: check the target directory, folder name, SKILL.md and account permissions; refresh the skill list. Check for duplicate Simar installations.
- MCP will not start: run the selected venv Python with `mcp-server/server.py --help`; ensure requirements are installed in that exact venv. Keep stdout for protocol traffic.
- HTTP rejected: check the Host/Origin values, `/mcp` path, trusted proxy and transport. Do not use a loopback URL from a remote cloud account.
- Research unavailable: produce a research plan or conditional draft and label facts unverified; do not substitute memory for current authority.
- PDF rejected: follow the specialized form workflow and human review; do not force the file through a generic converter.
- Existing skill: the installer deliberately stops. Back up the exact prior skill folders before updating.

Run the included checks with Python 3.11 or later after installing development dependencies:

```sh
.venv/bin/python -m pip install pytest -r pdf-requirements.txt
.venv/bin/python -m pytest -q tests
```

Try one case-audit request, one NOC-duty comparison, one source-verification request and a synthetic form draft before client use. Confirm the output preserves facts, distinguishes source evidence, refuses invented authorities and leaves human approval pending.

The MIT text is in LICENSE; attribution and third-party boundaries are in NOTICE.md. Preserve those files when sharing or selling copies.
