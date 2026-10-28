#!/usr/bin/env python3
"""Inspect/fill standard AcroForms as unsigned drafts requiring human review.

Uses pypdf. Does not execute Adobe validation, XFA, JavaScript or calculations.
Run inspect first. Values are read from a private JSON file, never CLI arguments.
"""
import argparse
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from pypdf import PdfReader, PdfWriter


def object_key(obj):
    ref = getattr(obj, "indirect_reference", None)
    return (ref.idnum, ref.generation) if ref else ("direct", id(obj))


def qualified_name(obj):
    parts, seen = [], set()
    while obj is not None:
        obj = obj.get_object()
        key = object_key(obj)
        if key in seen:
            raise ValueError("Cyclic form field parents.")
        seen.add(key)
        if obj.get("/T") is not None:
            parts.append(str(obj["/T"]))
        obj = obj.get("/Parent")
    return ".".join(reversed(parts))


def inherited(obj, key, default=None):
    seen = set()
    while obj is not None:
        obj = obj.get_object()
        identity = object_key(obj)
        if identity in seen:
            raise ValueError("Cyclic form field parents.")
        seen.add(identity)
        if key in obj:
            return obj[key]
        obj = obj.get("/Parent")
    return default


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def inventory(reader):
    root = reader.root_object
    acro = root.get("/AcroForm")
    reasons, fields, known, visited = [], {}, set(), set()
    if reader.is_encrypted:
        raise ValueError("Encrypted/restricted PDF requires an authorized separate workflow.")
    acro = acro.get_object() if acro else {}
    if not acro.get("/Fields"):
        reasons.append("No usable canonical AcroForm field tree.")
    if "/XFA" in acro:
        reasons.append("XFA requires a compatible application.")
    if acro.get("/CO"):
        reasons.append("Calculated fields require application validation.")
    if root.get("/Perms"):
        reasons.append("Certification/permission restrictions require separate review.")
    names = root.get("/Names")
    if names and names.get_object().get("/JavaScript"):
        reasons.append("Document JavaScript requires application validation.")
    opening = root.get("/OpenAction")
    if opening and isinstance(opening.get_object(), dict) and opening.get_object().get("/S") == "/JavaScript":
        reasons.append("Document JavaScript requires application validation.")

    def walk(ref):
        obj = ref.get_object()
        key = object_key(obj)
        if key in visited:
            raise ValueError("Repeated or cyclic field-tree reference.")
        visited.add(key)
        known.add(key)
        if obj.get("/AA") or obj.get("/A"):
            reasons.append("Field actions require application validation.")
        kids = [item.get_object() for item in obj.get("/Kids", [])]
        child_names = any("/T" in child for child in kids)
        kind = inherited(obj, "/FT")
        if "/T" in obj and kind and not child_names:
            name = qualified_name(obj)
            if name in fields:
                raise ValueError("Duplicate canonical field name: " + name)
            flags = int(inherited(obj, "/Ff", 0))
            options = []
            for option in inherited(obj, "/Opt", []):
                options.append(str(option[0] if isinstance(option, list) else option))
            fields[name] = {
                "object": obj, "type": str(kind), "flags": flags,
                "required": bool(flags & 2), "read_only": bool(flags & 1),
                "max_length": inherited(obj, "/MaxLen"), "options": options,
                "widgets": [], "value": inherited(obj, "/V"),
            }
            if kind == "/Sig" and inherited(obj, "/V"):
                reasons.append("Existing digital signature must not be invalidated.")
        for child in kids:
            walk(child)

    for item in acro.get("/Fields", []):
        walk(item)
    for page_number, page in enumerate(reader.pages, 1):
        if page.get("/AA"):
            reasons.append("Page actions require application validation.")
        for ref in page.get("/Annots", []):
            widget = ref.get_object()
            if widget.get("/Subtype") != "/Widget":
                continue
            owner = widget
            while "/T" not in owner and owner.get("/Parent"):
                owner = owner["/Parent"].get_object()
            name = qualified_name(owner)
            if object_key(owner) not in known or name not in fields:
                raise ValueError("Orphaned or ambiguous widget needs explicit field-tree review.")
            if object_key(owner) != object_key(fields[name]["object"]):
                raise ValueError("Widget and canonical field disagree: " + name)
            if widget.get("/AA") or widget.get("/A"):
                reasons.append("Widget actions require application validation.")
            fields[name]["widgets"].append((page_number, widget))
    return fields, sorted(set(reasons))


def public_inventory(fields, reasons):
    result = []
    for name, field in fields.items():
        options = list(field["options"])
        if field["type"] == "/Btn":
            options = sorted({str(key)
                for _, widget in field["widgets"]
                for key in (widget.get("/AP", {}).get("/N", {}) or {}).keys()})
        result.append({
            "name": name, "type": field["type"],
            "pages": sorted({p for p, _ in field["widgets"]}),
            "required": field["required"], "read_only": field["read_only"],
            "max_length": field["max_length"], "options": options,
            "is_signature": field["type"] == "/Sig",
        })
    return {"supported_standard_form": not reasons, "limitations": reasons, "fields": result}


def validate_values(fields, values):
    if not isinstance(values, dict) or not values:
        raise ValueError("Provide a nonempty JSON object of exact field names and confirmed answers.")
    for name, value in values.items():
        if name not in fields:
            raise ValueError("Unknown or nonterminal field: " + name)
        field = fields[name]
        kind, flags = field["type"], field["flags"]
        if field["read_only"]:
            raise ValueError("Read-only field: " + name)
        if kind == "/Sig" or (kind == "/Btn" and flags & (1 << 16)):
            raise ValueError("Signature/action fields cannot be autofilled: " + name)
        if not field["widgets"]:
            raise ValueError("No visible widget for field: " + name)
        if kind == "/Tx":
            if not isinstance(value, str):
                raise ValueError("Text must be a string, preserving identifiers and leading zeros: " + name)
            if field["max_length"] is not None and len(value) > int(field["max_length"]):
                raise ValueError("Text exceeds maximum field length; do not truncate: " + name)
        elif kind == "/Ch":
            selected = value if isinstance(value, list) else [value]
            if not all(isinstance(item, str) for item in selected):
                raise ValueError("Choice values must be strings: " + name)
            if isinstance(value, list) and not flags & (1 << 21):
                raise ValueError("Field does not support multiple choices: " + name)
            editable = bool(flags & (1 << 18))
            if not editable and any(item not in field["options"] for item in selected):
                raise ValueError("Use the exact inspected export option: " + name)
        elif kind == "/Btn":
            if not isinstance(value, str):
                raise ValueError("Use the exact inspected button export state, such as /Yes or /Off.")
            states = {str(key) for _, widget in field["widgets"]
                      for key in widget.get("/AP", {}).get("/N", {}).keys()}
            if value not in states:
                raise ValueError("Unknown checkbox/radio state: " + name)
        else:
            raise ValueError("Unsupported field type: " + name)


def verify_filled(reader, values):
    fields, reasons = inventory(reader)
    if reasons:
        raise ValueError("Output unexpectedly requires an unsupported workflow.")
    for name, value in values.items():
        field = fields[name]
        observed = inherited(field["object"], "/V")
        observed = list(map(str, observed)) if isinstance(observed, list) else str(observed)
        if observed != value:
            raise ValueError("Stored field value did not match: " + name)
        selected_count = 0
        for _, widget in field["widgets"]:
            appearance = widget.get("/AP", {}).get("/N")
            if appearance is None:
                raise ValueError("Missing visible appearance for field: " + name)
            appearance = appearance.get_object()
            if field["type"] == "/Btn":
                expected = value if value in appearance else "/Off"
                if str(widget.get("/AS", "/Off")) != expected:
                    raise ValueError("Button appearance mismatch: " + name)
                selected_count += expected != "/Off"
                stream = appearance.get(expected)
                if stream is None or not stream.get_object().get_data():
                    raise ValueError("Empty button appearance: " + name)
            else:
                effective = inherited(widget, "/V")
                effective = list(map(str, effective)) if isinstance(effective, list) else str(effective)
                if effective != value:
                    raise ValueError("Widget/canonical value mismatch: " + name)
                if not hasattr(appearance, "get_data") or not appearance.get_data():
                    raise ValueError("Empty text/choice appearance: " + name)
        if field["type"] == "/Btn" and value != "/Off" and not selected_count:
            raise ValueError("No selected button widget: " + name)
    return fields


def missing_required(fields):
    return [name for name, field in fields.items()
            if field["required"] and inherited(field["object"], "/V") in (None, "", "/Off", [])]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    inspect = sub.add_parser("inspect")
    inspect.add_argument("input", type=Path)
    fill = sub.add_parser("fill")
    fill.add_argument("input", type=Path)
    fill.add_argument("--values", type=Path, required=True)
    fill.add_argument("--output", type=Path, required=True)
    fill.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    try:
        input_path = args.input.resolve()
        reader = PdfReader(input_path)
        if reader.is_encrypted:
            raise ValueError("Encrypted PDF requires an authorized separate workflow.")
        fields, reasons = inventory(reader)
        if args.action == "inspect":
            print(json.dumps(public_inventory(fields, reasons), indent=2, ensure_ascii=False))
            return 0
        if reasons:
            raise ValueError("Use the compatible application workflow: " + "; ".join(reasons))
        values_path = args.values.resolve()
        values = json.loads(values_path.read_text(encoding="utf-8"))
        validate_values(fields, values)
        output, report_path = args.output.resolve(), args.report.resolve()
        if output == report_path:
            raise ValueError("Output and report must be separate files.")
        for path in (output, report_path):
            if path.exists() or path in (input_path, values_path):
                raise ValueError("Refusing to overwrite an input, output or report.")
            if not path.parent.is_dir():
                raise ValueError("Create output/report parent directories first.")
        input_hash = sha256(input_path)
        writer = PdfWriter()
        writer.clone_document_from_reader(reader)
        writer.update_page_form_field_values(None, values, auto_regenerate=False)
        with tempfile.TemporaryDirectory(prefix="simar-form-") as temp:
            staged = Path(temp) / "draft.pdf"
            with staged.open("wb") as stream:
                writer.write(stream)
            reopened = PdfReader(staged)
            completed = verify_filled(reopened, values)
            if len(reopened.pages) != len(reader.pages):
                raise ValueError("Page count changed unexpectedly.")
            if sha256(input_path) != input_hash:
                raise ValueError("Input changed during processing.")
            report = {
                "status": "Draft - human review required",
                "human_review_required": True, "human_review_completed": False,
                "source_sha256": input_hash, "draft_sha256": sha256(staged),
                "pages": len(reopened.pages),
                "updated_fields": list(values),
                "unfilled_required_fields": missing_required(completed),
                "unsigned_signature_fields": [n for n, f in completed.items() if f["type"] == "/Sig"],
                "field_and_appearance_checks": "passed",
                "visual_review_required": True,
                "adobe_validation_performed": False,
                "signed_or_submitted": False,
            }
            with output.open("xb") as stream:
                stream.write(staged.read_bytes())
            with report_path.open("x", encoding="utf-8") as stream:
                json.dump(report, stream, indent=2, ensure_ascii=False)
            print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    except Exception as error:
        print("Form operation failed: " + str(error), file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
