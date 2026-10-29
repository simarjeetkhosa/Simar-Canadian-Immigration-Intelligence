# Security

## Current security update

Version 1.0.2 pins the optional PDF library to **pypdf 6.21.2**, replacing 6.10.0. GitHub Dependabot reported malformed-PDF processing vulnerabilities, including excessive runtime, infinite loops and memory consumption. The upstream release includes security fixes: https://github.com/py-pdf/pypdf/releases/tag/6.21.2.

Install the latest package and update the Python environment used by the helpers:

```sh
python -m pip install -r pdf-requirements.txt
python -c "import pypdf; print(pypdf.__version__)"
```

Use the Python executable from your actual virtual environment. It should report 6.21.2 for this release. Installing skill instructions alone does not update an existing Python environment. Earlier download archives contain the older dependency pin; use the current download linked in README.md.

## Handling untrusted documents

Process unknown PDFs in an isolated environment with appropriate file-size, memory and execution-time limits. Keep originals and review generated drafts. Library updates reduce known risk but do not establish that every document is safe.

## Report a vulnerability

Use this repository's GitHub Security tab and its private reporting option if available. Do not put credentials, client records or exploitable private details in public issues. For ordinary setup questions, see SUPPORT.md. No response-time guarantee is offered.
