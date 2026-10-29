# Release validation

## v1.0.3 workflow update — 29 October 2026

Adds substantive representative submissions, relationship chronology and marriage-evidence assessment, verified policy/case-law integration and refusal-file workflows. Skill metadata validation passed. All six existing compatibility/integration tests passed before packaging. These checks do not establish legal accuracy for a client case or compatibility with every AI host.


## v1.0.2 security update — 29 October 2026

Updated optional PDF dependency to pypdf 6.21.2, the version proposed by GitHub Dependabot for the reported vulnerabilities. Six tests passed on macOS with Python 3.14.2: the five existing MCP/installer/configuration tests plus a synthetic two-page AcroForm round trip. The new regression verifies saved field values, page count, appearance checks, unchanged source, pending human review, and refusal to overwrite an existing draft. The test environment used MCP 1.30.0, pypdf 6.21.2, Pillow 12.3.0, ReportLab 4.5.1 and img2pdf 0.6.3.

These checks confirm compatibility with the exercised workflows. They are not an exhaustive security audit, exploit test suite, visual form review or legal/portal validation. Earlier validation below is retained as historical context.

## Original v1.0.1 validation

Checked on 28 October 2026. Version 1.0.1.

This release updates the product, skill, companion, MCP display/configuration, template and package names to Simar Canadian Immigration Intelligence. The existing integration suite was rerun after the rename, including protection against duplicate installations under the earlier folder names. Public MCP tool names remain stable.

## Completed

- Validated both installed skill definitions and their relative references.
- Exercised the professional-role workflow on an RCIC-to-Claude/JR/Adobe/MIT scenario using an independent agent. It kept professional authority, tool availability, current research and human review distinct.
- Ran five integration tests: actual MCP stdio connection; actual Streamable HTTP connection and hostile Host rejection; installer preview/copy/existing-file protection; generated configuration parsing and overwrite refusal; and rejection of an unscoped network bind.
- Verified MCP initialization, tool listing, read-only annotations, document retrieval, local topic search, prompt retrieval and resource reading. Unknown IDs, traversal-style inputs, invalid search limits and empty queries were rejected; an unmatched query returned no results.
- Installed optional PDF dependencies in an isolated environment and ran the exported form helper on a synthetic two-page AcroForm. Stored-value and appearance checks passed, a missing required field was reported, human review remained pending, and no Adobe validation, signing or submission was claimed.
- Retained the previously exercised PDF helper workflows, including preservation of originals, unsupported-form rejection and explicit upload-size reporting. Fixtures and test client-like data are not distributed.

Test environment: Linux, Python 3.12, official MCP Python SDK 1.30.0, pypdf 6.10.0, Pillow 12.3.0, ReportLab 4.5.1 and img2pdf 0.6.3. The test suite requires Python 3.11 or later; the scripts target Python 3.10 or later. Review dependency security updates before deployment.

## Not claimed

This release has not been tested inside the recipient's Claude, ChatGPT, VS Code or other AI account; no remote service, tunnel or marketplace plugin has been deployed. Windows/macOS commands and configurations follow documented interfaces but were not executed on those operating systems here. Organizational permissions and client-version differences can affect installation.

The MCP server has no live case-law corpus, web search, scheduler, case-file tools or Adobe control. It exposes bundled workflow context and blank templates only. Current law, case treatment, program status and legal deadlines must be checked during each actual task. Passing software tests does not establish legal correctness, portal acceptance, form validation or human approval.

The automated PDF helper checks do not replace visual inspection of each actual final form and the appropriate human review. Government XFA/calculated/barcode forms require their specialized validation route. The current connected Adobe tool set was inspected; unattended XFA validation was not demonstrated.
