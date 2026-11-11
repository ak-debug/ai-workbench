"""Draw generic slide skeletons from scratch; never read a source screenshot."""
import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

NAVY, BLUE, CYAN = '#07182D', '#0A60FF', '#02C8FF'
GRAY, LIGHT, WHITE, MUTED = '#525E6C', '#F2F5F9', '#FFFFFF', '#A9B6C6'
SIZE = (1800, 1100)
SLIDE_SIZE = (860, 484)


def build(output, font_path, bold_font_path, overwrite=False):
    output = Path(output)
    if output.suffix.lower() != '.png':
        raise ValueError('Output must have a .png extension.')
    if output.exists() and not overwrite:
        raise FileExistsError('Preview exists; pass --overwrite only when authorized.')
    fonts = {}

    def font(size, bold=False):
        key = (size, bold)
        if key not in fonts:
            fonts[key] = ImageFont.truetype(str(bold_font_path if bold else font_path), size)
        return fonts[key]

    def label(draw, xy, value, size=18, color=NAVY, bold=False, max_width=None):
        face = font(size, bold)
        bounds = draw.textbbox(xy, value, font=face)
        if max_width is not None and bounds[2] - bounds[0] > max_width:
            raise ValueError(f'Preview label too wide: {value}')
        draw.text(xy, value, font=face, fill=color)

    def arrow(draw, start, end, color=BLUE):
        draw.line([start, end], fill=color, width=3)
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = (dx * dx + dy * dy) ** .5
        ux, uy = dx / length, dy / length
        draw.polygon([end,
                      (end[0] - 9 * ux + 4 * uy, end[1] - 9 * uy - 4 * ux),
                      (end[0] - 9 * ux - 4 * uy, end[1] - 9 * uy + 4 * ux)], fill=color)

    def card(draw, box, title, dark=False, lines=2):
        x, y, right, bottom = box
        draw.rounded_rectangle(box, radius=12, fill=NAVY if dark else LIGHT)
        draw.rectangle((x + 8, y, right - 8, y + 3), fill=CYAN if dark else BLUE)
        label(draw, (x + 16, y + 18), title, 18, CYAN if dark else BLUE, True,
              right - x - 32)
        # Placeholder bars communicate empty content slots, not real data.
        for i in range(lines):
            line_y = y + 65 + i * 28
            if line_y + 7 > bottom - 18:
                raise ValueError('Skeleton bars exceed card bounds.')
            draw.rounded_rectangle((x + 16, line_y, right - 35 - i * 20, line_y + 7),
                                   radius=3, fill=MUTED)

    def base(section, title, subtitle, takeaway):
        slide = Image.new('RGB', SLIDE_SIZE, WHITE)
        draw = ImageDraw.Draw(slide)
        draw.rectangle((30, 22, 72, 26), fill=BLUE)
        label(draw, (30, 38), section, 12, BLUE, True)
        label(draw, (30, 70), title, 26, NAVY, True, 800)
        label(draw, (30, 116), subtitle, 17, GRAY, max_width=800)
        draw.rounded_rectangle((30, 426, 830, 464), radius=6, fill=NAVY)
        draw.rectangle((30, 434, 33, 456), fill=CYAN)
        label(draw, (47, 435), takeaway, 17, WHITE, True, 770)
        label(draw, (30, 470), 'GENERIC SKELETON / NO REAL PRODUCT OR ORGANIZATIONAL DATA', 9, GRAY)
        return slide, draw

    slides = []
    slide, draw = base('01 / PROCESS FLOW', 'Show the path from input to outcome',
                       'Three editable cards; one clear direction.', 'One clear flow; one clear message.')
    for x, title, dark in [(30, 'INPUT', False), (308, 'PROCESS', True), (586, 'OUTCOME', False)]:
        card(draw, (x, 178, x + 244, 393), title, dark)
    arrow(draw, (280, 280), (302, 280))
    arrow(draw, (558, 280), (580, 280), CYAN)
    slides.append(slide)

    slide, draw = base('02 / SHARED HUB', 'Show how teams use a shared capability',
                       'Generic roles connect to a common function and result.', 'A simple hub makes shared responsibility visible.')
    for y, title in [(190, 'TEAM A'), (265, 'TEAM B'), (340, 'TEAM C')]:
        draw.rounded_rectangle((30, y, 235, y + 52), radius=8, fill=LIGHT)
        label(draw, (46, y + 15), title, 18, NAVY, True)
        arrow(draw, (241, y + 26), (286, 286))
    card(draw, (292, 178, 578, 393), 'SHARED CAPABILITY', True)
    arrow(draw, (584, 286), (620, 286), CYAN)
    card(draw, (626, 178, 830, 393), 'RESULT')
    slides.append(slide)

    slide, draw = base('03 / BEFORE AND AFTER', 'Make the proposed change easy to understand',
                       'Compare a current workflow with an illustrative proposal.', 'Distinguish current behavior from the proposed change.')
    for x, title, dark in [(30, 'CURRENT APPROACH', False), (440, 'PROPOSED APPROACH', True)]:
        draw.rounded_rectangle((x, 178, x + 390, 393), radius=12, fill=NAVY if dark else LIGHT)
        draw.rectangle((x + 8, 178, x + 382, 181), fill=CYAN if dark else BLUE)
        label(draw, (x + 16, 197), title, 18, CYAN if dark else BLUE, True)
        for j, role in enumerate(['ROLE A', 'ROLE B']):
            rx = x + 18 + j * 185
            draw.rounded_rectangle((rx, 247, rx + 169, 291), radius=6, fill=WHITE)
            label(draw, (rx + 12, 260), role, 16, NAVY, True)
            end = (x + 195, 325) if dark else (rx + 84, 325)
            arrow(draw, (rx + 84, 298), end, CYAN if dark else BLUE)
            if not dark:
                draw.rounded_rectangle((rx, 331, rx + 169, 368), radius=5, fill=NAVY)
                label(draw, (rx + 12, 340), 'INPUT', 16, WHITE)
        if dark:
            draw.rounded_rectangle((x + 35, 331, x + 355, 368), radius=5, fill=BLUE)
            label(draw, (x + 51, 340), 'SHARED CAPABILITY', 16, WHITE, True)
    slides.append(slide)

    slide, draw = base('04 / ROADMAP', 'Turn the next step into a clear roadmap',
                       'Four short actions with room for outcomes and measures.', 'Use evidence to decide what happens next.')
    centers = [121, 326, 531, 736]
    draw.line([(centers[0], 202), (centers[-1], 202)], fill=MUTED, width=3)
    for i, (x, title) in enumerate(zip([30, 235, 440, 645], ['DISCOVER', 'PILOT', 'MEASURE', 'SCALE'])):
        cx = centers[i]
        draw.ellipse((cx - 18, 184, cx + 18, 220), fill=CYAN if i == 3 else BLUE)
        label(draw, (cx - 6, 191), str(i + 1), 18, WHITE, True)
        card(draw, (x, 248, x + 183, 393), title, i == 3)
    slides.append(slide)

    canvas = Image.new('RGB', SIZE, '#DFE6EE')
    draw = ImageDraw.Draw(canvas)
    label(draw, (40, 20), 'MANAGEMENT SLIDES / GENERIC SKELETONS', 27, NAVY, True)
    for slide, xy in zip(slides, [(40, 90), (920, 90), (40, 598), (920, 598)]):
        canvas.paste(slide, xy)
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output, format='PNG', optimize=True)
    return output


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--font', required=True, type=Path, help='Locally installed regular TrueType font')
    parser.add_argument('--bold-font', required=True, type=Path, help='Locally installed bold TrueType font')
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    print(build(args.output, args.font, args.bold_font, args.overwrite))
