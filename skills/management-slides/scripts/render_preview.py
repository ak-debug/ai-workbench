"""Render a .pptx to PDF and PNG previews, plus contact sheets, so every slide can be inspected.

    python render_preview.py deck.pptx OUTDIR [--dpi 80] [--per-sheet 6]

Needs LibreOffice (`soffice`) and `pdftoppm` (poppler) on PATH. Writes OUTDIR/<deck>.pdf, OUTDIR/s-NN.png and
OUTDIR/sheetN.png (2 columns). Open the contact sheets for an overview, then individual PNGs at a higher --dpi
for any slide that needs a closer look. Uses a private LibreOffice profile so a running LibreOffice is not disturbed.
Scratch output belongs in the host's temporary area, not in the product repository.
"""
import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image


def run(deck, outdir, dpi, per_sheet):
    for tool in ('soffice', 'pdftoppm'):
        if not shutil.which(tool):
            sys.exit(f'{tool} not found on PATH: install LibreOffice and poppler, or state that the deck '
                     f'has not been visually validated.')
    outdir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='lo-profile-') as profile:
        subprocess.run(['soffice', f'-env:UserInstallation=file://{profile}', '--headless', '--convert-to', 'pdf',
                        '--outdir', str(outdir), str(deck)], check=True, capture_output=True)
    pdf = outdir / (deck.stem + '.pdf')
    for old in outdir.glob('s-*.png'):
        old.unlink()
    subprocess.run(['pdftoppm', '-r', str(dpi), '-png', str(pdf), str(outdir / 's')], check=True)
    pages = sorted(outdir.glob('s-*.png'))
    images = [Image.open(p) for p in pages]
    w, h = images[0].size
    for n, start in enumerate(range(0, len(images), per_sheet), 1):
        chunk = images[start:start + per_sheet]
        rows = (len(chunk) + 1) // 2
        sheet = Image.new('RGB', (w * 2 + 10, (h + 10) * rows), '#777777')
        for i, image in enumerate(chunk):
            sheet.paste(image, ((i % 2) * (w + 10), (i // 2) * (h + 10)))
        sheet.save(outdir / f'sheet{n}.png')
    print(f'{pdf}: {len(pages)} slides; contact sheets: {outdir}/sheet*.png')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('deck', type=Path)
    parser.add_argument('outdir', type=Path)
    parser.add_argument('--dpi', type=int, default=80)
    parser.add_argument('--per-sheet', type=int, default=6)
    args = parser.parse_args()
    run(args.deck, args.outdir, args.dpi, args.per_sheet)
