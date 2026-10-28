# Requested form filling and final human review

## Start filling when the user asks

A request to fill, prefill or auto-fill a form authorizes preparing the draft from supplied/authorized case information. It does not authorize a signature, attestation, submission, or a claim that human review occurred.

Identify the exact official form number/title, version, program, applicant/family member and submission route. Verify the current form and instructions when relevant. Read the actual file; do not assume two versions share field names. Use the PDF or document skill for the file format.

Build a field-to-source ledger with the field/page, proposed answer, source location and unresolved issue. Reuse confirmed case facts. Preserve names, identifiers and leading zeros; follow form-specific dates and answer formats. Treat OCR as tentative until compared with the original. Do not guess sensitive declarations, prior refusals, immigration history, family relationships, admissibility answers, dates or signatures. Do not automatically use “No” or “N/A” for missing information.

## Choose the supported route

| Form type | Action |
| --- | --- |
| Standard interactive AcroForm | Inspect field tree, widgets and options; fill a new editable draft using a capable PDF tool or the bundled helper; reopen and verify stored values and appearances |
| Flat PDF | Use a supported overlay/Adobe fill workflow only if the official process accepts it; align to the original page and label it as a draft, not as a validated interactive form |
| XFA, calculated, scripted or barcode-dependent form | Use a compatible Adobe workflow and the form's current instructions; generic PDF value insertion does not execute validation or generate valid barcodes |
| Online application form | Use an authorized connected/browser workflow when available; draft/save within scope and stop before attestation or submission pending the required human review |
| Signed, certified, restricted or locked document | Preserve the original; use an appropriate permitted editing workflow or obtain an editable source, without stripping protections or invalidating a signature silently |

Never route a fillable form through the supporting-document merge/compression helper. It deliberately rejects forms to preserve their structure.

## Standard AcroForm helper

Use `scripts/fill_pdf_form.py inspect input.pdf` to inventory exact fields, options and unsupported features. For a standard supported form, create a private JSON mapping from exact field names to confirmed string values or supported choice lists, then run:

```bash
python scripts/fill_pdf_form.py fill input.pdf \
  --values confirmed_fields.json \
  --output completed_draft.pdf --report review_manifest.json
```

The helper preserves the original and keeps the output interactive. It rejects ambiguous/orphaned fields, signatures, XFA and scripted/calculated documents that require a separate workflow. Repair genuinely broken field trees through the PDF skill only after inspecting canonical fields and widgets; never attach duplicate fields blindly.

The helper checks exact names, read-only flags, choice/button values, text length, stored values and visible appearance streams. It produces a review manifest and hashes, not a legal or Adobe validation certificate. Render every completed page to check clipping, overflow, font/glyph errors, checkbox/radio state, date formats and missing content.

## Adobe Acrobat / Reader

Discover current Adobe tools and confirm connection before using them. An installed Adobe connector is not proof that it can fill fields, handle XFA or execute a form's validation. Inspect the actual capability and prefer it when sufficient. If unavailable or insufficient, continue supported local filling and prepare a field-by-field handoff for Adobe-required steps; state the exact limitation.

Use [Adobe's interactive/flat-form guidance](https://helpx.adobe.com/reader/desktop/fill-forms.html) and the current official form instructions. For IRCC barcode forms, check [IRCC's validation guidance](https://ircc.canada.ca/english/helpcentre/answer.asp?qnum=1523). Complete the required Validate action in a compatible application, inspect errors and generated barcode pages, save, reopen and recheck. Do not fabricate barcodes or represent a static overlay as validated.

Do not print-to-PDF, flatten, compress or remove scripts from a barcode/XFA form to force it through a generic filler. Do not automatically lower application security settings or install an obsolete Adobe version. If the supported application cannot be controlled in the current environment, provide the prepared answers and exact remaining validation/review steps; never pretend Adobe was opened.

## Mandatory human review before use

This is Simar's explicit workflow requirement. Deliver completed forms as **Draft - human review required** in the accompanying message and review manifest; do not add an obstructive watermark to an official form.

Provide:
- The draft and its form/version identity.
- Fields populated, missing and conflicting, with a source-based review checklist.
- Any unchecked required fields and any software/validation limitations.
- Confirmation that signatures, attestations and submission have not been performed unless separately authorized after the review.
- The exact version/hash to which any later approval applies.

Require the applicant and/or appropriate authorized human reviewer to check all answers, declarations, dates, selected options, supporting evidence and validation results. Record human approval only when actually received for that version. Do not infer it from earlier general permission to fill forms. Any later substantive change requires review of the changed version.

After human review, follow the specific official signing/submission procedure and the user's separate applicable authorization. Preparing or checking a signature field does not authorize signing on the person's behalf.
