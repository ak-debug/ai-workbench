"""Design kit for editable executive slides: type scale, grid, real text measurement, fit-checked primitives.

Why this exists: slides looked cramped and inconsistent because every layout picked its own font sizes and
coordinates, and nothing checked that text fitted. This module fixes that at the source.

* ONE type scale (`TYPE`). Nothing on a slide is smaller than `TYPE['label']`, except the footer.
* ONE grid (`L`, `R`, `TOP`, `BOTTOM`, `GUT`). Every slide's content starts and ends at the same heights.
* Text is MEASURED with Arial's real glyph widths (`line_count`, `text_height`). A primitive that cannot fit its
  text records a fit error; call `finish()` after building so every overflow is reported at once.
  Fix overflow by cutting words (move detail to notes) or enlarging the panel. Never by shrinking type.

Primitives keep card text inside its shape and return ordinary shapes/groups, so everything stays editable.
Requires python-pptx and Pillow. Rendering is still the final check: measured fit is a strong guard, not proof.
"""
import re
from pathlib import Path

from PIL import ImageFont
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

# ------------------------------------------------------------------ tokens
NAVY, BLUE, CYAN = '07182D', '0A60FF', '02C8FF'
GRAY, LIGHT, WHITE, MUTED = '525E6C', 'F2F5F9', 'FFFFFF', 'A9B6C6'
SOFT, EDGE, DASH, PILL_GRAY, ROW_ALT = 'E8F0FF', 'DFE6EF', '8A96A3', 'D1D5DB', 'F7F9FC'

TYPE = {          # points. Six sizes carry the whole deck (display and lead are for the cover only).
    'display': 44,    # cover title
    'lead': 24,       # cover subtitle and pull-quote
    'title': 28,      # slide headline, bold, one line
    'heading': 18,    # card headings, takeaway, panel titles, bold
    'body': 16,       # card body, subtitle
    'dense': 14,      # table cells, diagram node text, mock artefacts
    'label': 12,      # CAPS labels, pills, legends, diagram sub-labels. The minimum for content
    'footer': 10,     # source + page footer only
}
TITLE, HEAD, BODY, DENSE, LABEL, FOOT = (TYPE[k] for k in ('title', 'heading', 'body', 'dense', 'label', 'footer'))
LINE = 1.2        # line-height factor used for measuring (Arial renders at about 1.15)

W, H = 13.333333, 7.5
L, R = .5, 12.83
CW = R - L        # 12.33 content width
TOP, BOTTOM = 2.3, 5.95   # content band; takeaway strip sits at 6.15
GUT = .25

ROLE_STYLE = {    # fill, outline, dashed, label colour, sub-label colour (system diagrams)
    'input': (WHITE, BLUE, False, NAVY, GRAY),
    'step': (NAVY, None, False, WHITE, MUTED),
    'handoff': (BLUE, None, False, WHITE, 'DCE8FF'),
    'optional': (WHITE, DASH, True, NAVY, GRAY),
}

# ------------------------------------------------------------------ measurement
_FONT_FILES = {
    False: ['/System/Library/Fonts/Supplemental/Arial.ttf', '/Library/Fonts/Arial.ttf',
            'C:/Windows/Fonts/arial.ttf', '/usr/share/fonts/truetype/msttcorefonts/Arial.ttf',
            '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'],
    True: ['/System/Library/Fonts/Supplemental/Arial Bold.ttf', '/Library/Fonts/Arial Bold.ttf',
           'C:/Windows/Fonts/arialbd.ttf', '/usr/share/fonts/truetype/msttcorefonts/Arial_Bold.ttf',
           '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'],
}
_fonts = {}


def _font(bold):
    if bold not in _fonts:
        for path in _FONT_FILES[bold]:
            if Path(path).exists():
                _fonts[bold] = ImageFont.truetype(path, 100)
                break
        else:
            raise RuntimeError('No Arial (or Liberation Sans) font found for text measurement.')
    return _fonts[bold]


def text_width(value, size, bold=False):
    """Width in inches of one unwrapped string (no ** markup)."""
    return _font(bold).getlength(value) / 100 * size / 72


def _words(value, bold=False):
    words, cur = [], []
    for i, part in enumerate(str(value).split('**')):
        is_bold = bold or i % 2 == 1
        for piece in re.split(r'(\s+)', part):
            if not piece:
                continue
            if piece.isspace():
                if cur:
                    words.append(cur)
                    cur = []
            else:
                cur.append((piece, is_bold))
    if cur:
        words.append(cur)
    return words


def line_count(value, size, width, bold=False):
    """Wrapped line count for one paragraph in a box `width` inches wide. `**x**` marks bold runs."""
    avail, space = width * .98, text_width(' ', size)
    lines, used = 1, 0.0
    for word in _words(value, bold):
        w = sum(text_width(t, size, b) for t, b in word)
        if used == 0:
            used = w
        elif used + space + w <= avail:
            used += space + w
        else:
            lines, used = lines + 1, w
    return lines


def text_height(paras, size, width, space=6, bold=False):
    """Height in inches for paragraphs at `size`, `space` points between paragraphs."""
    paras = paras if isinstance(paras, list) else [paras]
    lines = sum(line_count(p, size, width, bold) for p in paras)
    return (lines * size * LINE + space * max(len(paras) - 1, 0)) / 72


# ------------------------------------------------------------------ fit errors
FIT = []
_ctx = {'slide': 0}


def _need(name, need, have):
    if need > have + .02:
        FIT.append(f"slide {_ctx['slide']}: '{name}' needs {need:.2f} in of height, has {have:.2f} in")


def finish():
    """Raise one error listing every overflow found while building. Call after the last slide."""
    if FIT:
        problems, FIT[:] = list(FIT), []
        raise ValueError('Text does not fit. Cut words or enlarge the panel, do not shrink type:\n  - '
                         + '\n  - '.join(problems))


# ------------------------------------------------------------------ primitives
def rgb(value):
    return RGBColor.from_string(value)


def add_runs(para, value, size, color, bold=False, bold_color=None):
    for i, part in enumerate(str(value).split('**')):
        if not part:
            continue
        run = para.add_run()
        run.text = part
        run.font.name = 'Arial'
        run.font.size = Pt(size)
        run.font.bold = bold or i % 2 == 1
        run.font.color.rgb = rgb((bold_color or color) if i % 2 == 1 else color)


def fill_frame(frame, paras, size, color, bold=False, bold_color=None, space=6,
               align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    frame.clear()
    frame.word_wrap = True
    frame.vertical_anchor = anchor
    paras = paras if isinstance(paras, list) else [paras]
    for i, value in enumerate(paras):
        para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        para.alignment = align
        para.space_after = Pt(space if i < len(paras) - 1 else 0)
        add_runs(para, value, size, color, bold, bold_color)


def flatten(shape):
    """Remove the theme style reference (drop shadow, theme line/font colours). Fill, line and text colours
    are always set explicitly, so the shape looks identical in PowerPoint, Keynote and LibreOffice."""
    style = shape._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style')
    if style is not None:
        shape._element.remove(style)


def rect(slide, x, y, w, h, fill, name='panel', rounded=False, radius=.08, outline=None, dashed=False,
         width=1.25):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.name = name
    flatten(shape)
    shape.fill.solid()
    shape.fill.fore_color.rgb = rgb(fill)
    if outline:
        shape.line.color.rgb = rgb(outline)
        shape.line.width = Pt(width)
        if dashed:
            shape.line.dash_style = MSO_LINE.DASH
    else:
        shape.line.fill.background()
    if rounded:
        shape.adjustments[0] = min(.5, radius / max(min(w, h), .1))
    return shape


def tb(slide, x, y, w, h, paras, size=BODY, color=GRAY, bold=False, name='text', bold_color=None, space=6,
       align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, check=True):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    shape.name = name
    frame = shape.text_frame
    frame.margin_left = frame.margin_right = frame.margin_top = frame.margin_bottom = 0
    fill_frame(frame, paras, size, color, bold, bold_color, space, align, anchor)
    if check:
        _need(name, text_height(paras, size, w, space, bold), h)
    return shape


def shape_text(shape, paras, size, color, bold=False, bold_color=None, space=6, align=PP_ALIGN.LEFT,
               anchor=MSO_ANCHOR.MIDDLE, pad=(.12, .06), check=True, name=None):
    """Put live text inside an existing shape (so the text moves with it)."""
    frame = shape.text_frame
    frame.margin_left = frame.margin_right = Inches(pad[0])
    frame.margin_top = frame.margin_bottom = Inches(pad[1])
    fill_frame(frame, paras, size, color, bold, bold_color, space, align, anchor)
    if check:
        width = shape.width / 914400 - 2 * pad[0]
        _need(name or shape.name, text_height(paras, size, width, space, bold) + 2 * pad[1],
              shape.height / 914400)
    return shape


def _items(body, size, dark, space):
    """Normalise a card body to [(text, size, colour, space_after)]."""
    body = body if isinstance(body, list) else ([body] if body else [])
    items = []
    for value in body:
        t, sz, col, sp = ((value if isinstance(value, tuple) else (value,)) + (None,) * 3)[:4]
        items.append((t, sz or size, col or (WHITE if dark else GRAY), space if sp is None else sp))
    return items


def card_height(heading, body, width, size=BODY, head_size=HEAD, pad=.25, space=6, top_extra=0):
    """Height in inches a card needs for this text at this width. Use it to size cards from their content."""
    inner = width - 2 * pad
    need = pad * 1.4 + top_extra
    if heading:
        need += text_height(heading, head_size, inner, 0, True) + 6 / 72
    items = _items(body, size, False, space)
    for i, (t, sz, _col, sp) in enumerate(items):
        need += text_height(t, sz, inner, 0) + (0 if i == len(items) - 1 else sp / 72)
    return need


def center_y(height):
    """Top edge that centres a block of `height` inches in the content band."""
    return TOP + max(BOTTOM - TOP - height, 0) / 2


def card(slide, x, y, w, h, heading, body, dark=False, size=BODY, head_size=HEAD, name=None, pad=.25,
         space=6, accent=True, lead_color=None, head_color=None, top_extra=0, align=PP_ALIGN.LEFT):
    """Rounded card. Heading and body are ONE text frame inside the card shape. Returns the shape.

    A body item is a string, or a tuple (text, size, colour, space_after_pt) where any value after the text may
    be None. Use a tuple for a caption line such as a source.
    size='auto' uses the heading size (18) when it fits and the body size (16) otherwise, so a sparse card is
    not left a third empty. It never goes below the body size."""
    if size == 'auto':
        size = HEAD if card_height(heading, body, w, HEAD, head_size, pad, space, top_extra) <= h else BODY
    shape = rect(slide, x, y, w, h, NAVY if dark else LIGHT, name or f'card-{heading or "body"}', True)
    items = _items(body, size, dark, space)
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.TOP
    frame.margin_left = frame.margin_right = Inches(pad)
    frame.margin_top = Inches(pad * .8 + top_extra)
    frame.margin_bottom = Inches(pad * .6)
    inner = w - 2 * pad
    first = True
    if heading:
        para = frame.paragraphs[0]
        para.alignment = align
        para.space_after = Pt(6)
        add_runs(para, heading, head_size, head_color or (CYAN if dark else BLUE), True)
        first = False
    need = pad * 1.4 + top_extra
    if heading:
        need += text_height(heading, head_size, inner, 0, True) + 6 / 72
    for i, (t, sz, col, sp) in enumerate(items):
        para = frame.paragraphs[0] if first and i == 0 else frame.add_paragraph()
        para.alignment = align
        last = i == len(items) - 1
        para.space_after = Pt(0 if last else sp)
        add_runs(para, t, sz, col, False, lead_color or (CYAN if dark else NAVY))
        need += text_height(t, sz, inner, 0) + (0 if last else sp / 72)
    _need(shape.name, need, h)
    parts = [shape]
    if accent:
        parts.append(rect(slide, x, y, w, .055, CYAN if dark else BLUE, 'card-accent'))
    slide.shapes.add_group_shape(parts).name = shape.name
    return shape


def pill(slide, x, y, value, fill=SOFT, color=BLUE, h=.3, size=LABEL, name='pill', width=None, bold=True):
    w = width or text_width(value, size, bold) + .3
    shape = rect(slide, x, y, w, h, fill, name, True, radius=h / 2)
    shape_text(shape, value, size, color, bold, align=PP_ALIGN.CENTER, pad=(.1, 0), space=0)
    shape.text_frame.word_wrap = False
    return shape


def hairline(slide, x, y, w, color=EDGE, name='rule'):
    return rect(slide, x, y, w, .02, color, name)


def label(slide, x, y, w, value, color=BLUE, name='label'):
    """CAPS section label, 12 pt bold."""
    return tb(slide, x, y, min(w, text_width(value, LABEL, True) + .15), .22, value, LABEL, color, True, name)


def labelled_rule(slide, x, y, w, value, color=BLUE):
    """CAPS label with a thin rule under it: groups the cards below."""
    label(slide, x, y, w, value, color, 'group-label')
    rect(slide, x, y + .29, w, .025, color, 'group-rule')


# ------------------------------------------------------------------ scenario / tag badges
BADGE_H, NUM_W = .3, .46


def badge_width(sid, name=''):
    return NUM_W + (text_width(name, LABEL, True) + .42 if name else 0)


def badge(slide, x, y, sid, name='', h=BADGE_H, on_dark=False):
    """Navy tag pill (S1) with an optional light name pill, grouped. Returns total width.
    on_dark=True draws a cyan pill with navy text, so it stays visible on a navy panel."""
    parts = []
    if name:
        w = badge_width(sid, name) - NUM_W + .1
        parts.append(pill(slide, x + NUM_W - .1, y, name, SOFT, NAVY, h, name=f'badge-{sid}-name', width=w))
        parts[-1].text_frame.margin_left = Inches(.2)
    fill, color = (MUTED, WHITE) if sid == 'ALL' else ((CYAN, NAVY) if on_dark else (NAVY, CYAN))
    num = pill(slide, x, y, sid, fill, color, h, name=f'badge-{sid}', width=NUM_W + (.1 if sid == 'ALL' else 0))
    parts.append(num)
    if len(parts) > 1:
        slide.shapes.add_group_shape(parts).name = f'tag-{sid}'
    return badge_width(sid, name)


def badges_right(slide, x_right, y, sids, on_dark=False):
    """Compact tags, right-aligned to x_right."""
    x = x_right - len(sids) * NUM_W - (len(sids) - 1) * .06
    for sid in sids:
        badge(slide, x, y, sid, on_dark=on_dark)
        x += NUM_W + .06


# ------------------------------------------------------------------ connectors
def _site(shape, index):
    x, y, w, h = shape.left, shape.top, shape.width, shape.height
    return [(x + w // 2, y), (x, y + h // 2), (x + w // 2, y + h), (x + w, y + h // 2)][index]


def link(slide, start, end, color=BLUE, dashed=False, head=True, width=2, name='flow-arrow'):
    """Connector between (shape, site) glue points or (x, y) inch points. Sites: 0 top, 1 left, 2 bottom, 3 right."""
    points = [_site(*p) if hasattr(p[0], 'left') else (Inches(p[0]), Inches(p[1])) for p in (start, end)]
    straight = abs(points[0][0] - points[1][0]) < 9000 or abs(points[0][1] - points[1][1]) < 9000
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT if straight else MSO_CONNECTOR.ELBOW,
                                      points[0][0], points[0][1], points[1][0], points[1][1])
    line.name = name
    if hasattr(start[0], 'left'):
        line.begin_connect(*start)
    if hasattr(end[0], 'left'):
        line.end_connect(*end)
    line.line.color.rgb = rgb(color)
    line.line.width = Pt(width)
    if dashed:
        line.line.dash_style = MSO_LINE.DASH
    if head:
        arrow = OxmlElement('a:tailEnd')
        arrow.set('type', 'triangle')
        arrow.set('w', 'med')
        arrow.set('len', 'med')
        line.line._get_or_add_ln().append(arrow)
    return line


def row_x(n, gap=GUT, left=L, width=CW, weights=None):
    """Left edges and widths for n equal (or weighted) columns."""
    weights = weights or [1] * n
    unit = (width - gap * (n - 1)) / sum(weights)
    out, x = [], left
    for wt in weights:
        out.append((x, unit * wt))
        x += unit * wt + gap
    return out


# ------------------------------------------------------------------ diagram node (system diagrams)
def node(slide, x, y, w, h, value, sub='', role='step', name=None, size=DENSE, sub_size=LABEL):
    fill, outline, dashed, label_color, sub_color = ROLE_STYLE[role]
    shape = rect(slide, x, y, w, h, fill, name or f'{role}-{value}', True, radius=.1, outline=outline,
                 dashed=dashed, width=1.5)
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.vertical_anchor = MSO_ANCHOR.MIDDLE
    frame.margin_left = frame.margin_right = Inches(.1)
    frame.margin_top = frame.margin_bottom = Inches(.05)
    para = frame.paragraphs[0]
    para.alignment = PP_ALIGN.CENTER
    para.space_after = Pt(2 if sub else 0)
    add_runs(para, value, size, label_color, True)
    need = text_height(value, size, w - .2, 0, True) + .1
    if sub:
        para2 = frame.add_paragraph()
        para2.alignment = PP_ALIGN.CENTER
        add_runs(para2, sub, sub_size, sub_color)
        need += text_height(sub, sub_size, w - .2, 0) + 2 / 72
    _need(shape.name, need, h)
    return shape


# ------------------------------------------------------------------ native table with measured row heights
def table(slide, x, y, widths, header, rows, size=DENSE, max_h=BOTTOM - TOP, first_col_bold=True,
          name='table', row_pad=.16, min_row=.42, head_h=.46, fill=True, max_row=1.0):
    """Native PowerPoint table. Row heights come from measured text, so rows never grow beyond the plan.
    With fill=True spare height is shared between rows (up to max_row each) so the table fills the content
    band instead of leaving dead space. Returns the total height."""
    head_h = max(head_h, max(text_height(h, size, widths[c] - .28, 0, True) for c, h in enumerate(header)) + row_pad)
    heights = []
    for row in rows:
        lines = max(text_height(cell, size, widths[c] - .28, 0, bold=(c == 0 and first_col_bold))
                    for c, cell in enumerate(row))
        heights.append(max(min_row, lines + row_pad))
    _need(name, head_h + sum(heights), max_h)
    if fill:
        spare = (max_h - head_h - sum(heights)) / len(rows)
        heights = [min(max_row, h + max(spare, 0)) if h + max(spare, 0) > h else h for h in heights]
    total = head_h + sum(heights)
    gf = slide.shapes.add_table(len(rows) + 1, len(widths), Inches(x), Inches(y), Inches(sum(widths)),
                                Inches(total))
    gf.name = name
    tbl = gf.table
    for i, wd in enumerate(widths):
        tbl.columns[i].width = Inches(wd)
    tbl.rows[0].height = Inches(head_h)
    for r, hgt in enumerate(heights, 1):
        tbl.rows[r].height = Inches(hgt)
    for r in range(len(rows) + 1):
        values = header if r == 0 else rows[r - 1]
        for c in range(len(widths)):
            cell = tbl.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = rgb(NAVY if r == 0 else (LIGHT if r % 2 else ROW_ALT))
            cell.margin_left = cell.margin_right = Inches(.14)
            cell.margin_top = cell.margin_bottom = Inches(.06)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            if r == 0:
                fill_frame(cell.text_frame, values[c], size, WHITE, True, space=0, anchor=MSO_ANCHOR.MIDDLE)
            else:
                first = c == 0 and first_col_bold
                fill_frame(cell.text_frame, values[c], size, NAVY if first else GRAY, first, BLUE, 0,
                           anchor=MSO_ANCHOR.MIDDLE)
    return total


# ------------------------------------------------------------------ slide frame
def notes(slide, value):
    frame = slide.notes_slide.notes_text_frame
    frame.clear()
    for i, line in enumerate(str(value).split('\n')):
        para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        run = para.add_run()
        run.text = line
        run.font.name = 'Arial'
        run.font.size = Pt(12)


def base(prs, spec, number, footer, cover=False):
    """Blank slide with the standard frame: accent, section label, headline, subtitle, takeaway, footer."""
    _ctx['slide'] = number
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = rgb(WHITE)
    rect(slide, L, .38, .65, .065, BLUE, 'top-accent')
    section = spec.get('section', spec.get('kicker', ''))
    tb(slide, L, .58, min(9.0, text_width(section, LABEL, True) + .15), .22, section, LABEL, BLUE, True, 'section')
    if not cover:
        tb(slide, L, .88, CW, .46, spec['title'], TITLE, NAVY, True, 'headline')
        if spec.get('subtitle'):
            tb(slide, L, 1.48, CW, .3, spec['subtitle'], BODY, GRAY, name='subtitle')
    if spec.get('takeaway'):
        strip = rect(slide, L, 6.15, CW, .6, NAVY, 'takeaway-strip', True, radius=.08)
        shape_text(strip, spec['takeaway'], HEAD, WHITE, True, pad=(.3, .05), name='takeaway')
        rect(slide, L, 6.26, .05, .38, CYAN, 'takeaway-accent')
    tb(slide, L, 6.98, 10.3, .2, spec.get('source', ''), FOOT, GRAY, name='source')
    tb(slide, 11.0, 6.98, R - 11.0, .2, f'{number:02d} · {footer}', FOOT, GRAY, name='footer',
       align=PP_ALIGN.RIGHT)
    notes(slide, spec.get('notes', ''))
    return slide
