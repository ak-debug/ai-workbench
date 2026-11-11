"""Editable executive-slide layouts. Facts and visual validation remain the agent's job."""
import argparse
import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
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
