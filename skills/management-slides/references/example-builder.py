"""Worked example: a small deck built on deck_kit. Copy it, replace the content, add layouts as needed.

    python example-builder.py OUTPUT.pptx

Shows the pattern every builder should follow: one function per layout, positions from the grid (TOP, BOTTOM,
row_x), text sizes from the type scale, `finish()` after the last slide so every overflow is reported at once.
Content here is generic on purpose.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))

import deck_kit as k  # noqa: E402
from deck_kit import BODY, BOTTOM, CYAN, DENSE, GUT, HEAD, L, TOP  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.util import Inches  # noqa: E402

SPEC = {
    'title': 'Example deck', 'footer': 'Example',
    'slides': [
        {'layout': 'cards', 'section': '01 / CAPABILITIES', 'title': 'Three capabilities cover the whole flow',
         'subtitle': 'Each capability has one owner and one measurable outcome.',
         'cards': [
             {'label': 'Detect', 'lines': ['Watches every source and finds the problem early.',
                                           'A person sees only what needs attention.',
                                           '**Outcome:** minutes, not days']},
             {'label': 'Decide', 'lines': ['Applies one shared rule set to every case.',
                                           'The same input always gets the same answer.',
                                           '**Outcome:** consistent calls']},
             {'label': 'Act', 'lines': ['Runs the approved step and records what happened.',
                                         'Anything unusual goes back to a person.',
                                         '**Outcome:** fewer manual steps'], 'dark': True}],
         'takeaway': 'One flow, three owners, measurable results.', 'source': 'Illustrative content',
         'notes': 'Sources and detail go here.'},
        {'layout': 'table', 'section': '02 / COMPARISON', 'title': 'The options differ in who decides',
         'subtitle': 'A table is fine for reference data.',
         'header': ['Option', 'Who decides', 'Typical use'], 'widths': [3.2, 4.2, 4.93],
         'rows': [['**A** Manual', 'A person, every time', 'Rare, high-risk changes'],
                  ['**B** Assisted', 'A person approves a suggestion', 'Routine changes with some risk'],
                  ['**C** Automatic', 'The system, with a report', 'Low-risk, reversible changes']],
         'takeaway': 'Match the option to the risk of the change.', 'source': 'Illustrative content'},
    ],
}


def cards(slide, s):
    for (x, w), c in zip(k.row_x(len(s['cards']), GUT), s['cards']):
        # equal heights, one shared top and bottom: every row of cards ends on BOTTOM.
        # size='auto' takes the 18 pt heading size when the text fits, else 16 pt: sparse cards are not left empty.
        k.card(slide, x, TOP, w, BOTTOM - TOP, c['label'], c['lines'], c.get('dark'), size='auto', head_size=HEAD,
               pad=.28, space=10, lead_color=CYAN if c.get('dark') else None, name=f"card-{c['label']}")


def table(slide, s):
    k.table(slide, L, TOP, s['widths'], s['header'], s['rows'], size=DENSE, name='comparison-table')


LAYOUTS = {'cards': cards, 'table': table}


def build(spec, output):
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(k.W), Inches(k.H)
    for number, item in enumerate(spec['slides'], 1):
        slide = k.base(prs, item, number, spec['footer'])
        LAYOUTS[item['layout']](slide, item)
    k.finish()          # raises one error listing every overflow
    prs.save(output)
    print('saved', output)


if __name__ == '__main__':
    build(SPEC, sys.argv[1] if len(sys.argv) > 1 else 'example.pptx')
