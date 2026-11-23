"""Editable executive-slide layouts. Facts and visual validation remain the agent's job."""
import argparse
import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.dml import MSO_LINE
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.xmlchemy import OxmlElement
from pptx.util import Inches, Pt

NAVY, BLUE, CYAN = '07182D', '0A60FF', '02C8FF'
GRAY, LIGHT, WHITE, MUTED = '525E6C', 'F2F5F9', 'FFFFFF', 'A9B6C6'
WIDTH, HEIGHT = 13.333333, 7.5


def rectangle(slide, x, y, w, h, fill, rounded=False, name='panel'):
    kind = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shape = slide.shapes.add_shape(kind, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.name = name
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor.from_string(fill)
    shape.line.fill.background()
    if rounded:
        shape.adjustments[0] = .10
    return shape


def text(slide, x, y, w, h, value, size=18, color=NAVY, bold=False, name='text'):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    shape.name = name
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = frame.margin_right = 0
    frame.margin_top = frame.margin_bottom = 0
    lines = value if isinstance(value, list) else str(value).split('\n')
    for i, line in enumerate(lines):
        para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        para.text = str(line)
        para.font.name = 'Arial'
        para.font.size = Pt(size)
        para.font.bold = bold
        para.font.color.rgb = RGBColor.from_string(color)
        para.space_after = Pt(9)
    return shape


def connector(slide, start, end, color=BLUE, directed=True):
    shape = slide.shapes.add_connector(
        MSO_CONNECTOR.STRAIGHT, Inches(start[0]), Inches(start[1]),
        Inches(end[0]), Inches(end[1]),
    )
    shape.name = 'editable-flow-connector'
    shape.line.color.rgb = RGBColor.from_string(color)
    shape.line.width = Pt(2)
    if directed:
        # DrawingML tailEnd is the connector's ending arrow; keep it editable.
        arrow = OxmlElement('a:tailEnd')
        arrow.set('type', 'triangle')
        arrow.set('w', 'sm')
        arrow.set('len', 'sm')
        shape.line._get_or_add_ln().append(arrow)
    return shape


def card(slide, x, y, w, h, data, size=18):
    dark = bool(data.get('dark'))
    parts = [
        rectangle(slide, x, y, w, h, NAVY if dark else LIGHT, True, 'card-background'),
        rectangle(slide, x, y, w, .055, CYAN if dark else BLUE, name='card-accent'),
        text(slide, x+.24, y+.25, w-.48, .7, data['label'],
             19, CYAN if dark else BLUE, True, 'card-heading'),
        text(slide, x+.24, y+1.02, w-.48, h-1.16, data.get('lines', []),
             size, WHITE if dark else GRAY, name='card-body'),
    ]
    group = slide.shapes.add_group_shape(parts)
    group.name = f"card-{data['label']}"
    return group


def graph_motif(slide, x, y):
    pts = [(x, y), (x+.42, y-.24), (x+.50, y+.30), (x-.25, y+.43)]
    for point in pts[1:]:
        connector(slide, pts[0], point, CYAN, False)
    for i, point in enumerate(pts):
        r = .12 if i == 0 else .07
        node = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(point[0]-r),
                                      Inches(point[1]-r), Inches(2*r), Inches(2*r))
        node.name = 'editable-graph-node'
        node.fill.solid()
        node.fill.fore_color.rgb = RGBColor.from_string(CYAN if i == 0 else BLUE)
        node.line.fill.background()


def base(prs, spec, number, footer):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = RGBColor.from_string(WHITE)
    rectangle(slide, .5, .4, .65, .065, BLUE, name='top-accent')
    text(slide, .5, .66, 12.3, .3, spec.get('section', ''), 11, BLUE, True)
    text(slide, .5, 1.1, 12.3, .83, spec['title'], 30, NAVY, True, 'headline')
    text(slide, .5, 1.98, 12.3, .52, spec.get('subtitle', ''), 17, GRAY)
    rectangle(slide, .5, 6.2, 12.33, .6, NAVY, True, 'takeaway-strip')
    rectangle(slide, .5, 6.31, .045, .36, CYAN, name='takeaway-accent')
    text(slide, .76, 6.35, 11.8, .37, spec['takeaway'], 18, WHITE, True)
    text(slide, .5, 7.05, 10.7, .22, spec.get('source', ''), 8, GRAY)
    text(slide, 11.5, 7.05, 1.34, .22, f'{number:02d} · {footer}', 7.5, GRAY)
    slide.notes_slide.notes_text_frame.text = spec.get('notes', '')
    return slide


def row_layout(slide, nodes, flow=False):
    if not 2 <= len(nodes) <= (4 if flow else 3):
        raise ValueError('Use 2–4 flow nodes or 2–3 cards.')
    gap = .45 if flow else .25
    w = (12.33-gap*(len(nodes)-1))/len(nodes)
    h = 3.10
    for i, node in enumerate(nodes):
        x = .5+i*(w+gap)
        card(slide, x, 2.78, w, h, node, 16 if len(nodes) == 4 else 17)
        if flow and i < len(nodes)-1:
            connector(slide, (x+w+.035, 4.08), (x+w+gap-.035, 4.08))


def hub_layout(slide, spec):
    agents = spec['agents']
    if not 2 <= len(agents) <= 3:
        raise ValueError('A management hub supports 2–3 agent cards.')
    center_y = 4.17
    for i, agent in enumerate(agents):
        y = 2.95+i*.88
        parts = [rectangle(slide, .5, y, 3.10, .65, LIGHT, True, 'role-background'),
                 text(slide, .72, y+.16, 2.66, .35, agent, 18, NAVY, True)]
        slide.shapes.add_group_shape(parts).name = f'role-{agent}'
        connector(slide, (3.63, y+.325), (4.58, center_y))
    hub = dict(spec['hub'], dark=True)
    card(slide, 4.65, 2.78, 3.85, 3.1, hub, 17)
    if spec.get('graph_motif', False):
        graph_motif(slide, 7.61, 5.32)
    connector(slide, (8.54, center_y), (9.10, center_y), CYAN)
    card(slide, 9.18, 2.78, 3.65, 3.1, spec['result'], 17)


def before_after(slide, spec):
    # Roles inside the two panels can vary; this depicts repeated vs shared routes.
    for x, data, shared in [(.5, spec['before'], False), (6.79, spec['after'], True)]:
        first_shape = len(slide.shapes)
        w = 6.04
        rectangle(slide, x, 2.78, w, 3.1, NAVY if shared else LIGHT, True)
        rectangle(slide, x, 2.78, w, .055, CYAN if shared else BLUE)
        text(slide, x+.24, 3.03, w-.48, .45, data['label'], 19,
             CYAN if shared else BLUE, True)
        text(slide, x+.24, 5.42, w-.48, .32, data['caption'], 17,
             WHITE if shared else GRAY)
        for i in range(2):
            ax = x+.40+i*2.87
            role = data.get('actors', ['Role A', 'Role B'])[i]
            parts = [rectangle(slide, ax, 3.70, 2.40, .55, WHITE, True, 'role-background'),
                     text(slide, ax+.12, 3.84, 2.16, .30, role, 17, NAVY, True)]
            slide.shapes.add_group_shape(parts).name = f'role-{role}'
            if shared:
                connector(slide, (ax+1.2, 4.28), (x+3.02, 4.60), CYAN)
            else:
                connector(slide, (ax+1.2, 4.28), (ax+1.2, 4.60), BLUE)
                parts = [rectangle(slide, ax, 4.65, 2.40, .53, NAVY, True, 'source-background'),
                         text(slide, ax+.12, 4.78, 2.16, .3, data.get('node_label', 'Input'), 17, WHITE)]
                slide.shapes.add_group_shape(parts).name = 'separate-source'
        if shared:
            parts = [rectangle(slide, x+1.03, 4.65, 3.98, .53, BLUE, True, 'source-background'),
                     text(slide, x+1.20, 4.78, 3.64, .3, data.get('node_label', 'Shared capability'), 17, WHITE, True)]
            slide.shapes.add_group_shape(parts).name = 'shared-source'
        slide.shapes.add_group_shape(list(slide.shapes)[first_shape:]).name = f"comparison-{data['label']}"


def roadmap(slide, spec):
    steps = spec['steps']
    if not 3 <= len(steps) <= 4:
        raise ValueError('Use 3–4 roadmap steps.')
    gap = .24
    w = (12.33-gap*(len(steps)-1))/len(steps)
    centers = [.5+i*(w+gap)+w/2 for i in range(len(steps))]
    connector(slide, (centers[0], 2.99), (centers[-1], 2.99), MUTED, False)
    for i, (cx, step) in enumerate(zip(centers, steps)):
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx-.23), Inches(2.76), Inches(.46), Inches(.46))
        dot.fill.solid()
        dot.fill.fore_color.rgb = RGBColor.from_string(CYAN if step.get('dark') else BLUE)
        dot.line.fill.background()
        number = text(slide, cx-.075, 2.835, .23, .28, str(i+1), 17, WHITE, True)
        slide.shapes.add_group_shape([dot, number]).name = f'roadmap-number-{i+1}'
        card(slide, .5+i*(w+gap), 3.5, w, 2.38, step, 16)


DASH, PILL_GRAY, PANEL_EDGE, SOFT_BLUE = '8A96A3', 'D1D5DB', 'DFE6EF', '9CC1FF'
ROLE_STYLE = {  # fill, outline, dashed, label colour, sub-label colour
    'input': (WHITE, BLUE, False, NAVY, GRAY),
    'step': (NAVY, None, False, WHITE, MUTED),
    'handoff': (BLUE, None, False, WHITE, 'DCE8FF'),
    'optional': (WHITE, DASH, True, NAVY, GRAY),
}
NODE_GAP, ARROW_GAP, MIN_NODE_H = .10, .27, .44


def _estimate_lines(chars, size, width):
    return max(1, -(-int(chars * size * .55 / 72 * 100) // int(max(width, .1) * 100)))


def _check_fit(data, w, h, size, sub_size):
    """Rough guard only: rendered review is still required."""
    inner = w - .12
    need = _estimate_lines(len(data['label']), size, inner) * size * 1.2
    if data.get('sub'):
        need += _estimate_lines(len(data['sub']), sub_size, inner) * sub_size * 1.2
    if need / 72 + .06 > h:
        raise ValueError(f"System node '{data['label']}' is too long for a {w:.2f}x{h:.2f} in box; shorten it.")


def _site(shape, index):
    x, y, w, h = shape.left, shape.top, shape.width, shape.height
    return [(x + w // 2, y), (x, y + h // 2), (x + w // 2, y + h), (x + w, y + h // 2)][index]


def link(slide, start, end, color=NAVY, dashed=False, head=True, width=1.75, name='flow-connector'):
    """Connector between (shape, site) glue points or (x, y) inch points.
    Sites are 0 top, 1 left, 2 bottom, 3 right. Glued ends follow moved nodes."""
    points = [_site(*p) if hasattr(p[0], 'left') else (Inches(p[0]), Inches(p[1])) for p in (start, end)]
    straight = abs(points[0][0] - points[1][0]) < 9000 or abs(points[0][1] - points[1][1]) < 9000
    shape = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT if straight else MSO_CONNECTOR.ELBOW,
                                       points[0][0], points[0][1], points[1][0], points[1][1])
    shape.name = name
    if hasattr(start[0], 'left'):
        shape.begin_connect(*start)
    if hasattr(end[0], 'left'):
        shape.end_connect(*end)
    shape.line.color.rgb = RGBColor.from_string(color)
    shape.line.width = Pt(width)
    if dashed:
        shape.line.dash_style = MSO_LINE.DASH
    if head:
        arrow = OxmlElement('a:tailEnd')
        arrow.set('type', 'triangle')
        arrow.set('w', 'med')
        arrow.set('len', 'med')
        shape.line._get_or_add_ln().append(arrow)
    return shape


def system_node(slide, x, y, w, h, data, role, name, anchor=MSO_ANCHOR.MIDDLE, size=None):
    fill, outline, dashed, label_color, sub_color = ROLE_STYLE[role]
    shape = rectangle(slide, x, y, w, h, fill, True, name)
    shape.adjustments[0] = min(.12, .10 / max(min(w, h), .1) * .5)
    if outline:
        shape.line.color.rgb = RGBColor.from_string(outline)
        shape.line.width = Pt(1.5)
        if dashed:
            shape.line.dash_style = MSO_LINE.DASH
    size = size or (12 if w < 1.9 else 13)
    sub_size = size - 2
    if not data.get('steps'):
        _check_fit(data, w, h, size, sub_size)
    frame = shape.text_frame
    frame.word_wrap = True
    frame.vertical_anchor = anchor
    frame.margin_left = frame.margin_right = Inches(.06)
    frame.margin_top = frame.margin_bottom = Inches(.04 if anchor == MSO_ANCHOR.MIDDLE else .10)
    for i, (value, bold, color, pt) in enumerate([(data['label'], True, label_color, size),
                                                  (data.get('sub', ''), False, sub_color, sub_size)]):
        if i and not value:
            break
        para = frame.paragraphs[0] if i == 0 else frame.add_paragraph()
        para.alignment = PP_ALIGN.CENTER
        run = para.add_run()
        run.text = value
        run.font.name, run.font.size, run.font.bold = 'Arial', Pt(pt), bold
        run.font.color.rgb = RGBColor.from_string(color)
    return shape


def engine_node(slide, x, y, w, h, data, name):
    """Navy card with a header and stacked blue sub-steps; grouped so it moves as one."""
    shape = system_node(slide, x, y, w, h, data, 'step', name, MSO_ANCHOR.TOP, 14)
    shape.adjustments[0] = .05
    steps = data['steps']
    top, gap = y + .62, .16
    step_h = (y + h - .15 - top - gap * (len(steps) - 1)) / len(steps)
    if step_h < MIN_NODE_H:
        raise ValueError(f"'{data['label']}' has too many sub-steps for the available height.")
    parts, previous = [shape], None
    for i, step in enumerate(steps):
        current = system_node(slide, x + .22, top + i * (step_h + gap), w - .44, step_h, step,
                              'handoff', f'{name}-step-{i + 1}', size=12)
        parts.append(current)
        if previous is not None:
            parts.append(link(slide, (previous, 2), (current, 0), SOFT_BLUE, width=1.5, name=f'{name}-step-arrow'))
        previous = current
    slide.shapes.add_group_shape(parts).name = name
    return shape


def system_layout(slide, spec):
    columns = spec['columns']
    if not 2 <= len(columns) <= 7:
        raise ValueError('A system diagram supports 2-7 columns.')
    alternate, legend = spec.get('alternate'), spec.get('legend')
    left, right, top = .5, 12.83, 2.78
    headers = any(c.get('header') for c in columns)
    height = 2.0 if alternate else (2.75 if legend else 3.2)
    rectangle(slide, left, top, right - left, height, LIGHT, True, 'system-container')
    container = slide.shapes[-1]
    container.adjustments[0] = .06
    container.line.color.rgb = RGBColor.from_string(BLUE)
    container.line.width = Pt(1.75)
    label = spec.get('container', {}).get('label', '').upper()
    if label:
        pill = system_node(slide, left + .27, top - .17, len(label) * .085 + .45, .33,
                           {'label': label}, 'handoff', 'system-label', size=9.5)
        pill.adjustments[0] = .5
    inner_top = top + .32 + (.3 if headers else 0)
    inner_h = height - (inner_top - top) - .12
    inner_x, inner_w = left + .15, right - left - .3
    unit = (inner_w - ARROW_GAP * (len(columns) - 1)) / sum(c.get('weight', 1) for c in columns)
    placed, x = [], inner_x
    for ci, column in enumerate(columns):
        w, nodes = unit * column.get('weight', 1), column['nodes']
        k = len(nodes)
        tall = bool(column.get('tall')) or any(n.get('steps') for n in nodes)
        gap = NODE_GAP if k > 1 else 0
        node_h = (inner_h - gap * (k - 1)) / k
        if not tall:
            node_h = min(node_h, 1.1 if k == 1 else .9)
        if node_h < MIN_NODE_H:
            raise ValueError(f'Column {ci + 1} has too many nodes for the available height.')
        y = inner_top + (inner_h - (node_h * k + gap * (k - 1))) / 2
        if column.get('header'):
            text(slide, x, top + .36, w, .22, column['header'].upper(), 9.5, GRAY, True, 'column-header')
        shapes = []
        for ni, data in enumerate(nodes):
            role = data.get('role', 'input' if ci == 0 else 'step')
            if role not in ROLE_STYLE:
                raise ValueError(f'Unknown node role: {role}')
            name = f"{role}-{data['label']}"
            nx, ny = x, y + ni * (node_h + gap)
            shapes.append(engine_node(slide, nx, ny, w, node_h, data, name) if data.get('steps')
                          else system_node(slide, nx, ny, w, node_h, data, role, name))
        placed.append((shapes, [n.get('role', 'input' if ci == 0 else 'step') for n in nodes]))
        x += w + ARROW_GAP
    for ci in range(len(columns) - 1):
        (a, a_roles), (b, b_roles) = placed[ci], placed[ci + 1]
        a_ids = [i for i, n in enumerate(columns[ci]['nodes']) if not n.get('no_out')]
        b_ids = [i for i, n in enumerate(columns[ci + 1]['nodes']) if not n.get('no_in')]
        if len(a_ids) == len(b_ids):
            pairs = list(zip(a_ids, b_ids))
        elif len(a_ids) == 1:
            pairs = [(a_ids[0], j) for j in b_ids]
        elif len(b_ids) == 1:
            pairs = [(i, b_ids[0]) for i in a_ids]
        else:
            raise ValueError(f'Columns {ci + 1} and {ci + 2} cannot be linked: use equal counts or a single node.')
        for i, j in pairs:
            dashed = 'optional' in (a_roles[i], b_roles[j])
            link(slide, (a[i], 3), (b[j], 1), DASH if dashed else NAVY, dashed)
    lane_top = top + height + .15
    if alternate:
        start_node, end_node = (placed[i][0][j] for i, j in
                                (alternate.get('from', [2, 0]), alternate.get('to', [len(columns) - 1, 0])))
        start_x, end_x = [(n.left + n.width / 2) / 914400 for n in (start_node, end_node)]
        alt_nodes = alternate['nodes']
        first_x, last_x = start_x + .55, end_x - .55
        if last_x - first_x < len(alt_nodes) * 1.1:
            raise ValueError('Alternate lane has too little horizontal room for its nodes.')
        caption = alternate.get('caption')
        pill_label = alternate.get('label', '').upper()
        pill = system_node(slide, first_x, lane_top, len(pill_label) * .085 + .45, .30,
                           {'label': pill_label}, 'optional', 'alternate-label', size=9.5)
        pill.adjustments[0] = .5
        pill.fill.fore_color.rgb = RGBColor.from_string(PILL_GRAY)
        pill.line.fill.background()
        node_y = lane_top + .36
        if caption:
            text(slide, first_x, node_y - .02, last_x - first_x, .22, caption, 10.5, GRAY, name='alternate-caption')
            node_y += .24
        alt_h = 6.08 - node_y
        gap = .22
        alt_w = min(2.3, (last_x - first_x - gap * (len(alt_nodes) - 1)) / len(alt_nodes))
        row = [system_node(slide, first_x + i * (alt_w + gap), node_y, alt_w, alt_h, data, 'optional',
                           f"optional-{data['label']}") for i, data in enumerate(alt_nodes)]
        mid_y = node_y + alt_h / 2
        link(slide, (start_node, 2), (start_x, mid_y), DASH, True, False, 1.5, 'alternate-drop')
        link(slide, (start_x, mid_y), (row[0], 1), DASH, True, True, 1.5, 'alternate-entry')
        for a, b in zip(row, row[1:]):
            link(slide, (a, 3), (b, 1), DASH, True, True, 1.5, 'alternate-step-arrow')
        link(slide, (row[-1], 3), (end_x, mid_y), DASH, True, False, 1.5, 'alternate-exit')
        link(slide, (end_x, mid_y), (end_node, 2), DASH, True, True, 1.5, 'alternate-return')
        legend_y, legend_x = lane_top, left
        if legend and start_x - left < 3.9:
            raise ValueError('The legend overlaps the alternate path: move the alternate source column right or drop the legend.')
    if legend:
        horizontal = not alternate
        row_h = .32
        box_w = 3.5 if not horizontal else right - left
        box_h = .24 + row_h * len(legend) if not horizontal else .42
        legend_y = lane_top if alternate else top + height + .12
        box = rectangle(slide, left, legend_y, box_w, box_h, WHITE, True, 'legend-background')
        box.adjustments[0] = .08
        box.line.color.rgb = RGBColor.from_string(PANEL_EDGE)
        box.line.width = Pt(1)
        parts, step_x = [box], (box_w - .3) / len(legend)
        for i, entry in enumerate(legend):
            if entry['role'] not in ROLE_STYLE:
                raise ValueError(f"Unknown legend role: {entry['role']}")
            ex = left + .24 + (i * step_x if horizontal else 0)
            ey = legend_y + (.12 if not horizontal else .1) + (0 if horizontal else i * row_h)
            fill, outline, dashed, _, _ = ROLE_STYLE[entry['role']]
            swatch = rectangle(slide, ex, ey + .03, .46, .17, fill, True, 'legend-swatch')
            swatch.adjustments[0] = .3
            if outline:
                swatch.line.color.rgb = RGBColor.from_string(outline)
                swatch.line.width = Pt(1.25)
                if dashed:
                    swatch.line.dash_style = MSO_LINE.DASH
            parts += [swatch, text(slide, ex + .59, ey, (step_x if horizontal else box_w) - .9, .24,
                                   entry['text'], 10.5, GRAY, name='legend-label')]
        slide.shapes.add_group_shape(parts).name = 'legend'


def build(spec, output, overwrite=False):
    output = Path(output)
    if output.suffix.lower() != '.pptx':
        raise ValueError('Output must have a .pptx extension.')
    if output.exists() and not overwrite:
        raise FileExistsError(f'{output} exists; use --overwrite only when authorized.')
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(WIDTH), Inches(HEIGHT)
    prs.core_properties.title = spec.get('title', 'Management summary')
    prs.core_properties.author = spec.get('author', '')
    slides = spec.get('slides', [])
    if not slides:
        raise ValueError('Spec needs at least one slide.')
    for number, item in enumerate(slides, 1):
        slide = base(prs, item, number, spec.get('footer', ''))
        layout = item.get('layout', 'cards')
        if layout in ('cards', 'flow'):
            row_layout(slide, item['cards' if layout == 'cards' else 'nodes'], layout == 'flow')
        elif layout == 'hub':
            hub_layout(slide, item)
        elif layout == 'before-after':
            before_after(slide, item)
        elif layout == 'roadmap':
            roadmap(slide, item)
        elif layout == 'system':
            system_layout(slide, item)
        else:
            raise ValueError(f'Unknown layout: {layout}')
        for shape in slide.shapes:
            if min(shape.left, shape.top) < 0 or shape.left+shape.width > prs.slide_width+100 or shape.top+shape.height > prs.slide_height+100:
                raise ValueError(f'Slide {number}: {shape.name} is off canvas.')
    output.parent.mkdir(parents=True, exist_ok=True)
    prs.save(output)
    print(f'Saved {len(slides)} editable slides: {output}')
    print('Bounds checked. Render and inspect every slide: text fit has not been validated.')
    return prs


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--spec', required=True, type=Path, help='Vetted content JSON; see references/example-deck.json')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--overwrite', action='store_true', help='Only use for an authorized replacement')
    args = parser.parse_args()
    build(json.loads(args.spec.read_text()), args.output, args.overwrite)
