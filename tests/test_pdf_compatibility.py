"""Verify the form helper still works with the patched PDF dependency."""
import hashlib
import json
import subprocess
import sys
from pathlib import Path

from pypdf import PdfReader
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / 'skills/simar-canadian-immigration-intelligence/scripts/fill_pdf_form.py'


def test_form_round_trip_and_overwrite_protection(tmp_path):
    source = tmp_path / 'source.pdf'
    c = canvas.Canvas(str(source))
    c.drawString(50, 800, 'Synthetic test form')
    c.acroForm.textfield(name='full_name', x=50, y=700, width=200,
                        height=20, fieldFlags='required')
    c.showPage()
    c.drawString(50, 800, 'Synthetic second page')
    c.save()
    original = source.read_bytes()
    values = tmp_path / 'values.json'
    values.write_text(json.dumps({'full_name': 'Synthetic Example'}))
    output, report = tmp_path / 'draft.pdf', tmp_path / 'review.json'
    command = [sys.executable, str(HELPER), 'fill', str(source), '--values',
               str(values), '--output', str(output), '--report', str(report)]
    result = subprocess.run(command, capture_output=True, text=True, timeout=30)
    assert result.returncode == 0, result.stderr
    reader = PdfReader(output)
    assert len(reader.pages) == 2
    assert reader.get_fields()['full_name']['/V'] == 'Synthetic Example'
    review = json.loads(report.read_text())
    assert review['human_review_required'] is True
    assert review['human_review_completed'] is False
    assert review['field_and_appearance_checks'] == 'passed'
    assert review['source_sha256'] == hashlib.sha256(original).hexdigest()
    assert source.read_bytes() == original
    saved = output.read_bytes()
    repeat = subprocess.run(command, capture_output=True, text=True, timeout=30)
    assert repeat.returncode != 0
    assert output.read_bytes() == saved
