#!/usr/bin/env python3
"""Assemble supporting-document PDFs/images with a verified user-supplied size limit.

Requires pypdf, Pillow and reportlab. Optional: img2pdf, OCRmyPDF, Ghostscript.
Never overwrites inputs or existing outputs. Interactive/encrypted PDFs are refused.
OCR and text detection are reported separately from visual readability.
"""
import argparse
import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from xml.sax.saxutils import escape

from pypdf import PdfReader, PdfWriter

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".bmp", ".webp", ".gif"}
SUPPORTED = IMAGE_EXTS | {".pdf"}
DPI_LADDER = [300, 250, 200, 165, 150, 120, 100]


def file_hash(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_static_pdf(path):
    reader = PdfReader(path)
    if reader.is_encrypted:
        raise ValueError(f"Encrypted PDF requires a separate workflow: {Path(path).name}")
    if reader.trailer["/Root"].get("/AcroForm"):
        raise ValueError(f"Interactive or signature-bearing PDF requires separate handling: {Path(path).name}")
    for page in reader.pages:
        for annotation in page.get("/Annots", []):
            if annotation.get_object().get("/Subtype") == "/Widget":
                raise ValueError(f"Form/signature widget requires separate handling: {Path(path).name}")
    if not reader.pages:
        raise ValueError(f"Empty PDF: {Path(path).name}")
    return reader


def image_to_pdf(source, output):
    from PIL import Image, ImageOps, ImageSequence
    # A single JPEG can be embedded without re-encoding if img2pdf is installed.
    if source.suffix.lower() in {".jpg", ".jpeg"}:
        try:
            import img2pdf
            with Image.open(source) as check:
                orientation = check.getexif().get(274, 1)
            if orientation == 1:
                output.write_bytes(img2pdf.convert(str(source)))
                return
        except ImportError:
            pass
    frames = []
    with Image.open(source) as image:
        for frame in ImageSequence.Iterator(image):
            frame = ImageOps.exif_transpose(frame.copy()).convert("RGBA")
            background = Image.new("RGB", frame.size, "white")
            background.paste(frame, mask=frame.getchannel("A"))
            frames.append(background)
    if not frames:
        raise ValueError(f"No image frames: {source.name}")
    frames[0].save(output, "PDF", save_all=True, append_images=frames[1:],
                   resolution=200.0, quality=95)
    for frame in frames:
        frame.close()


def index_pdf(entries, output, title, font_path=None):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    labels = [title] + [item["source"] for item in entries]
    font_name = "Helvetica"
    if font_path:
        font_name = "SimarIndex"
        pdfmetrics.registerFont(TTFont(font_name, str(font_path)))
        glyphs = pdfmetrics.getFont(font_name).face.charToGlyph
        unsupported = {c for label in labels for c in label if not c.isspace() and ord(c) not in glyphs}
        if unsupported:
            raise ValueError("Index font lacks characters used in the title or source names.")
    elif any(ord(c) > 126 or ord(c) < 32 for label in labels for c in label):
        raise ValueError("Use ASCII index labels or supply --index-font with suitable glyphs; originals are unchanged.")
    styles = getSampleStyleSheet()
    for style in styles.byName.values():
        style.fontName = font_name
    styles["BodyText"].fontSize = 9
    styles["BodyText"].leading = 12
    styles["BodyText"].wordWrap = "CJK"
    document = SimpleDocTemplate(str(output), pagesize=letter,
                                 topMargin=48, bottomMargin=48, leftMargin=48, rightMargin=48)
    rows = [[Paragraph("Document", styles["BodyText"]), Paragraph("Starts on page", styles["BodyText"])]]
    for entry in entries:
        rows.append([Paragraph(escape(entry["source"]), styles["BodyText"]),
                     str(entry["start_page"])])
    table = Table(rows, colWidths=[414, 102], repeatRows=1, hAlign="LEFT")
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E7EDF3")),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F9FB")]),
        ("GRID", (0, 0), (-1, -1), .4, colors.HexColor("#CBD5E1")),
        ("FONTNAME", (0, 0), (-1, -1), font_name),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    document.build([Paragraph(escape(title), styles["Title"]), Spacer(1, 14), table])


def source_entries(normalized, offset):
    entries, page = [], offset + 1
    for source, pdf, count in normalized:
        entries.append({"source": source.name, "start_page": page, "page_count": count})
        page += count
    return entries


def merge(normalized, output, title, add_index, font_path):
    index_path, offset = output.with_name("index.pdf"), 0
    if add_index:
        for _ in range(8):
            index_pdf(source_entries(normalized, offset), index_path, title, font_path)
            count = len(PdfReader(index_path).pages)
            if count == offset:
                break
            offset = count
        else:
            raise ValueError("Index pagination did not stabilize.")
    entries = source_entries(normalized, offset)
    writer = PdfWriter()
    if add_index:
        for page in PdfReader(index_path).pages:
            writer.add_page(page)
        writer.add_outline_item("Index", 0)
    for entry, (_, pdf, _) in zip(entries, normalized):
        for page in PdfReader(pdf).pages:
            writer.add_page(page)
        writer.add_outline_item(Path(entry["source"]).stem, entry["start_page"] - 1)
    writer.add_metadata({"/Title": title, "/Producer": "Simar Canadian Immigration Intelligence document assembly"})
    with output.open("wb") as stream:
        writer.write(stream)
    return entries, offset


def run_optional(command):
    try:
        return subprocess.run(command, capture_output=True, text=True, timeout=300)
    except (OSError, subprocess.TimeoutExpired):
        return None


def text_lengths(path):
    return [len((page.extract_text() or "").strip()) for page in PdfReader(path).pages]


def valid_candidate(path, expected):
    try:
        observed = text_lengths(path)
        return len(observed) == len(expected) and all(
            not before or after for before, after in zip(expected, observed))
    except Exception:
        return False


def apply_ocr(source, output, lang, warnings):
    if not shutil.which("ocrmypdf"):
        warnings.append("OCRmyPDF unavailable: no new OCR layer added.")
        return source, "unavailable"
    result = run_optional(["ocrmypdf", "--skip-text", "--optimize", "1",
                           "--output-type", "pdf", "--language", lang, "--quiet",
                           str(source), str(output)])
    if result and result.returncode == 0 and output.exists() and valid_candidate(output, text_lengths(source)):
        return output, "completed"
    warnings.append("OCR failed or failed integrity checks: retained pre-OCR pages.")
    return source, "failed"


def compress(source, workdir, limit, minimum_dpi, warnings):
    if source.stat().st_size <= limit:
        return source, None
    if not shutil.which("gs"):
        warnings.append("Ghostscript unavailable: size reduction was not attempted.")
        return source, None
    best, best_dpi = source, None
    expected = text_lengths(source)
    ladder = sorted({dpi for dpi in DPI_LADDER if dpi >= minimum_dpi} | {minimum_dpi}, reverse=True)
    for dpi in ladder:
        candidate = workdir / f"compressed-{dpi}.pdf"
        command = ["gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.6",
                   "-dNOPAUSE", "-dBATCH", "-dQUIET", "-dSAFER", "-dAutoRotatePages=/None",
                   "-dDetectDuplicateImages=true",
                   "-dColorImageDownsampleType=/Bicubic", "-dDownsampleColorImages=true",
                   f"-dColorImageResolution={dpi}",
                   "-dGrayImageDownsampleType=/Bicubic", "-dDownsampleGrayImages=true",
                   f"-dGrayImageResolution={dpi}",
                   "-dMonoImageDownsampleType=/Subsample", "-dDownsampleMonoImages=true",
                   f"-dMonoImageResolution={max(300, dpi)}",
                   f"-sOutputFile={candidate}", str(source)]
        result = run_optional(command)
        if not result or result.returncode != 0 or not candidate.exists():
            warnings.append(f"Compression at {dpi} DPI failed.")
            continue
        if not valid_candidate(candidate, expected):
            warnings.append(f"Compression at {dpi} DPI failed page/text checks.")
            continue
        if candidate.stat().st_size < best.stat().st_size:
            best, best_dpi = candidate, dpi
        if best.stat().st_size <= limit:
            break
    return best, best_dpi


def restore_outlines(source, output, entries, index_pages, title):
    writer = PdfWriter()
    for page in PdfReader(source).pages:
        writer.add_page(page)
    if index_pages:
        writer.add_outline_item("Index", 0)
    for entry in entries:
        writer.add_outline_item(Path(entry["source"]).stem, entry["start_page"] - 1)
    writer.add_metadata({"/Title": title, "/Producer": "Simar Canadian Immigration Intelligence document assembly"})
    with output.open("wb") as stream:
        writer.write(stream)


def main():
    parser = argparse.ArgumentParser(description="Merge supporting documents using the actual upload size limit.")
    parser.add_argument("inputs", nargs="*", help="PDF/image inputs in the required order.")
    parser.add_argument("--output", required=True)
    limits = parser.add_mutually_exclusive_group(required=True)
    limits.add_argument("--max-mb", type=float, help="Decimal MB: 1 MB = 1,000,000 bytes.")
    limits.add_argument("--max-bytes", type=int, help="Exact portal byte limit.")
    parser.add_argument("--from-dir")
    parser.add_argument("--title")
    parser.add_argument("--index", action="store_true")
    parser.add_argument("--index-font", type=Path)
    parser.add_argument("--no-ocr", action="store_true")
    parser.add_argument("--lang", default="eng")
    parser.add_argument("--min-dpi", type=int, default=150)
    parser.add_argument("--report-json", type=Path)
    args = parser.parse_args()
    if args.max_mb is not None and (not math.isfinite(args.max_mb) or args.max_mb <= 0):
        parser.error("--max-mb must be finite and positive.")
    limit = args.max_bytes if args.max_bytes is not None else int(args.max_mb * 1_000_000)
    if limit <= 0 or not 72 <= args.min_dpi <= 600:
        parser.error("Use a positive size limit and --min-dpi between 72 and 600.")
    output = Path(args.output).resolve()
    inputs = [Path(value).resolve() for value in args.inputs]
    if args.from_dir:
        directory = Path(args.from_dir).resolve()
        if not directory.is_dir():
            parser.error("--from-dir is not a directory.")
        inputs += sorted((p.resolve() for p in directory.iterdir()
                          if p.is_file() and p.suffix.lower() in SUPPORTED
                          and p.resolve() != output), key=lambda p: p.name)
    if not inputs or len(set(inputs)) != len(inputs):
        parser.error("Provide at least one input; duplicate inputs are not accepted.")
    for source in inputs:
        if not source.is_file() or source.suffix.lower() not in SUPPORTED:
            parser.error(f"Missing or unsupported input: {source.name}")
    report_path = args.report_json.resolve() if args.report_json else None
    for destination in [output] + ([report_path] if report_path else []):
        if destination in inputs or destination.exists():
            parser.error("Refusing to overwrite an input or an existing output/report.")
    if report_path == output:
        parser.error("The report and PDF must have different paths.")
    if not output.parent.is_dir() or (report_path and not report_path.parent.is_dir()):
        parser.error("Create the destination directory first.")
    warnings = []
    hashes = {str(p): file_hash(p) for p in inputs}
    title = args.title or output.stem
    try:
        with tempfile.TemporaryDirectory(prefix="simar-assembly-") as temp:
            workdir = Path(temp)
            normalized = []
            for index, source in enumerate(inputs):
                pdf = source
                if source.suffix.lower() != ".pdf":
                    pdf = workdir / f"image-{index}.pdf"
                    image_to_pdf(source, pdf)
                count = len(read_static_pdf(pdf).pages)
                normalized.append((source, pdf, count))
            merged = workdir / "merged.pdf"
            entries, index_pages = merge(normalized, merged, title, args.index, args.index_font)
            expected = text_lengths(merged)
            if args.no_ocr:
                stage, ocr_status = merged, "skipped"
            else:
                stage, ocr_status = apply_ocr(merged, workdir / "ocr.pdf", args.lang, warnings)
            candidate, dpi = compress(stage, workdir, limit, args.min_dpi, warnings)
            staged = workdir / "final.pdf"
            restore_outlines(candidate, staged, entries, index_pages, title)
            if not valid_candidate(staged, expected):
                raise ValueError("Final page/text integrity check failed.")
            lengths = text_lengths(staged)
            if not all(file_hash(Path(p)) == digest for p, digest in hashes.items()):
                raise ValueError("An input changed during assembly; no output published.")
            # Exclusive creation also protects against a destination appearing mid-run.
            with output.open("xb") as stream, staged.open("rb") as source:
                shutil.copyfileobj(source, stream)
            size = output.stat().st_size
            report = {
                "output": str(output), "bytes": size, "limit_bytes": limit,
                "within_limit": size <= limit, "pages": len(lengths),
                "index_pages": index_pages, "source_map": entries,
                "ocr_status": ocr_status,
                "pages_with_text": [i + 1 for i, count in enumerate(lengths) if count],
                "pages_without_detectable_text": [i + 1 for i, count in enumerate(lengths) if not count],
                "text_characters_per_page": lengths, "image_dpi_used": dpi,
                "input_hashes_unchanged": True, "visual_review_required": True,
                "warnings": warnings,
            }
            if report_path:
                with report_path.open("x", encoding="utf-8") as stream:
                    json.dump(report, stream, indent=2, ensure_ascii=False)
            print(json.dumps(report, indent=2, ensure_ascii=False))
            if size > limit:
                print("OVER LIMIT: preserve required evidence; review quality and the portal's permitted alternatives.", file=sys.stderr)
                return 2
            return 0
    except Exception as error:
        print(f"Assembly failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
