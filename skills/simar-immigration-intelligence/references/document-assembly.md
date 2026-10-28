# Assemble supporting-document PDFs

Use this workflow for requested merging, ordering, indexing, compression or OCR of supporting documents. Use the PDF skill for inspection and visual verification. Do not treat an upload size limit as universal: confirm the exact portal field, permitted format and byte/MB limit from the current instructions or user-provided portal details.

## Prepare the package

Read the relevant document checklist and establish the intended field and order. Keep one logical upload requirement per package. Inventory every file and page; identify unreadable scans, rotated pages, duplicates, missing pages and sensitive labels. Do not remove required evidence merely to meet a size target.

Preserve original files. Use a new output path and neutral descriptive filenames. Keep signed, encrypted, interactive or barcode-dependent forms in their prescribed format and handling workflow; the bundled script refuses encrypted PDFs and form/signature widgets instead of silently invalidating them. Inspect unusual or dynamic forms separately.

The script supports static PDFs and common raster images, including multi-frame TIFF/GIF inputs. Convert DOCX or other unsupported formats through the appropriate document tools first and check the result.

## Run the bundled helper

Use the current skill directory as the base for `scripts/assemble_docs.py`. Confirm dependencies in the active runtime. Required Python packages: pypdf, Pillow and reportlab. Optional tools: OCRmyPDF for adding OCR, Ghostscript for compression, and img2pdf for lossless JPEG embedding when suitable. Prefer installed runtime dependencies and install only what is needed; do not use blanket system upgrades or `--break-system-packages`.

Example after confirming the field really permits 4,000,000 bytes:

```bash
python scripts/assemble_docs.py \
  --output supporting_documents.pdf --max-bytes 4000000 \
  --index --title "Supporting Documents" \
  --report-json supporting_documents_report.json \
  cover_letter.pdf employment_letter.pdf statement_scan.tiff
```

Use `--max-mb` for decimal MB (1,000,000 bytes) or `--max-bytes` for an exact limit. A limit is required. Use `--no-ocr` to skip OCR, `--lang` for installed OCR language packs, and `--min-dpi` to set a chosen lower bound for image downsampling. The default minimum is 150 DPI; lower it only when a visual check supports readability.

`--from-dir` selects supported files in filename order and excludes the output path; explicit input order is preferable for application packages. Duplicate inputs and existing output/report paths are rejected. Non-ASCII index labels require a suitable `--index-font`; review script shaping and glyph rendering visually, especially for Punjabi. Do not rename or alter original client evidence just to satisfy an index label.

## Interpret the result honestly

The JSON report includes actual bytes, limit status, total/index pages, per-source start pages and counts, OCR status, pages with/without detectable text, compression DPI and warnings. Source hashes are checked for changes.

- A successful size check is not proof of legibility, completeness, accurate OCR or portal acceptance.
- Text detected on one page does not make every page searchable. Review the per-page results, including mixed image/text pages.
- Missing OCR software produces a clear warning and preserves the merge; it does not pretend OCR succeeded.
- Ghostscript is optional. If compression is unavailable or insufficient, the report says so. Exit code 2 means the output remains over the limit (or invalid CLI arguments when no report was created); do not label it upload-ready.
- OCR is a convenience layer, not a certified transcription. Do not use its recognition errors to alter the source record.
- Compression can affect raster detail and PDF features. Do not promise visually unchanged content merely because page counts and text-presence checks passed.

## Verify before delivery

Reopen the exact final PDF. Check total pages, source order/counts, bookmarks, index destinations including all index pages, and detected text on each expected page. Render and inspect every final page for small-print readability, signatures/stamps/photos, orientation, clipping and blank/missing content.

Check actual output bytes against the portal limit, including any required margin. If the file cannot fit while remaining legible and complete, explain the specific constraint and follow permitted alternatives. Do not split uploads into fields the portal does not offer, omit pages or continue lowering quality blindly.

Save requested final deliverables through the normal artifact-saving workflow. Keep diagnostics and client filenames private unless useful to the user. Uploading or submitting a completed package is a separate action requiring the user's applicable authorization.
