"""Lint a finished .pptx against the management-slides design rules.

    python lint_deck.py deck.pptx [--max-words 120] [--min-size 12]

Reads the file itself (not the spec that produced it), so it also checks decks built by hand or by another tool.
Checks, per slide: font family, smallest font, text that would overflow its shape (measured with Arial metrics),
partially overlapping text shapes, shapes off the canvas, and words on the slide.
Exit code 1 if any ERROR is found. WARN items need a look but do not fail.
A clean lint is not proof the slide looks right: still render and inspect every slide.
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

from pptx import Presentation
from pptx.util import Emu

sys.path.insert(0, str(Path(__file__).parent))
import deck_kit as k  # noqa: E402

FOOTER_NAMES = ('footer', 'source')
FRAME_NAMES = ('footer', 'source', 'section', 'headline', 'subtitle', 'takeaway')   # not counted as body words


def paragraph_value(para):
    runs = [r for r in para.runs if r.text]
    if not runs:
        return '', 0, False
    size = max((r.font.size.pt if r.font.size else 18) for r in runs)
    all_bold = all(r.font.bold for r in runs)
    if all_bold:
        return ''.join(r.text for r in runs), size, True
    return ''.join(f'**{r.text}**' if r.font.bold else r.text for r in runs), size, False


def frame_height(frame, width_in):
    total, first = 0.0, True
    for para in frame.paragraphs:
        value, size, bold = paragraph_value(para)
        if not value:
            continue
        if not first:
            total += (para.space_after.pt if para.space_after is not None else 0) / 72
        total += k.text_height(value, size, width_in, 0, bold)
        first = False
    return total


def walk(shapes, out):
    for shape in shapes:
        if shape.shape_type == 6:
            walk(shape.shapes, out)
        else:
            out.append(shape)


def lint(path, max_words, min_size):
    prs = Presentation(path)
    errors, warns = [], []
    sizes = Counter()
    sw, sh = prs.slide_width, prs.slide_height
    for number, slide in enumerate(prs.slides, 1):
        flat = []
        walk(slide.shapes, flat)
        words = 0
        text_boxes = []
        for shape in flat:
            name = shape.name
            tag = f'slide {number} [{name}]'
            if shape.left < -100 or shape.top < -100 or shape.left + shape.width > sw + 100 \
                    or shape.top + shape.height > sh + 100:
                errors.append(f'{tag}: off the canvas')
            frames = []
            if shape.has_text_frame and shape.text_frame.text.strip():
                frames.append((shape.text_frame, shape.width, shape.height,
                               shape.text_frame.margin_left, shape.text_frame.margin_right,
                               shape.text_frame.margin_top, shape.text_frame.margin_bottom))
                text_boxes.append(shape)
            if getattr(shape, 'has_table', False) and shape.has_table:
                tbl = shape.table
                for r, row in enumerate(tbl.rows):
                    for c, cell in enumerate(row.cells):
                        if cell.text_frame.text.strip():
                            frames.append((cell.text_frame, tbl.columns[c].width, row.height,
                                           cell.margin_left, cell.margin_right, cell.margin_top,
                                           cell.margin_bottom))
            for frame, w, h, ml, mr, mt, mb in frames:
                is_footer = any(n in name.lower() for n in FOOTER_NAMES)
                for para in frame.paragraphs:
                    for run in para.runs:
                        if not run.text.strip():
                            continue
                        if not any(n in name.lower() for n in FRAME_NAMES):
                            words += len(run.text.split())
                        if run.font.name != 'Arial':
                            errors.append(f'{tag}: font is {run.font.name!r}, not Arial')
                        size = run.font.size.pt if run.font.size else None
                        if size is None:
                            errors.append(f'{tag}: run without an explicit font size')
                            continue
                        sizes[size] += len(run.text.split())
                        if size < min_size and not (is_footer and size >= k.FOOT):
                            errors.append(f'{tag}: {size:g} pt is below the {min_size:g} pt minimum')
                inner_w = Emu(w - ml - mr).inches
                need = frame_height(frame, inner_w) + Emu(mt + mb).inches
                have = Emu(h).inches
                if need > have + .03:
                    errors.append(f'{tag}: text needs {need:.2f} in but the shape is {have:.2f} in tall')
        # partial overlaps between text shapes (full containment is a card holding a label: fine)
        for i, a in enumerate(text_boxes):
            for b in text_boxes[i + 1:]:
                ox = min(a.left + a.width, b.left + b.width) - max(a.left, b.left)
                oy = min(a.top + a.height, b.top + b.height) - max(a.top, b.top)
                if a.name.startswith('badge-') and b.name.startswith('badge-'):
                    continue
                if ox > 9000 and oy > 9000:
                    inside = (a.left <= b.left and a.top <= b.top and a.left + a.width >= b.left + b.width
                              and a.top + a.height >= b.top + b.height) or \
                             (b.left <= a.left and b.top <= a.top and b.left + b.width >= a.left + a.width
                              and b.top + b.height >= a.top + a.height)
                    if not inside:
                        warns.append(f'slide {number}: [{a.name}] overlaps [{b.name}] '
                                     f'({Emu(ox).inches:.2f} x {Emu(oy).inches:.2f} in)')
        if words > max_words and number > 1:
            warns.append(f'slide {number}: {words} body words (guide: 35-65 for a management slide, warn above '
                         f'{max_words}); move detail to notes')
    return errors, warns, sizes


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('deck', type=Path)
    parser.add_argument('--max-words', type=int, default=110, help='body words per slide before a warning')
    parser.add_argument('--min-size', type=float, default=k.LABEL)
    args = parser.parse_args()
    errors, warns, sizes = lint(args.deck, args.max_words, args.min_size)
    scale = ', '.join(f'{s:g}' for s in sorted(sizes))
    print(f'{args.deck.name}: font sizes used (pt): {scale}')
    for w in warns:
        print('WARN ', w)
    for e in errors:
        print('ERROR', e)
    print(f'{len(errors)} error(s), {len(warns)} warning(s)')
    sys.exit(1 if errors else 0)


if __name__ == '__main__':
    main()
