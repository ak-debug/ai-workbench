"""Structural regression checks; these do not replace rendered visual review."""
import importlib.util
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.oxml.ns import qn

MODULE = Path(__file__).with_name('build_deck.py')
loader = importlib.util.spec_from_file_location('deck_builder', MODULE)
builder = importlib.util.module_from_spec(loader)
loader.loader.exec_module(builder)
EXAMPLE = MODULE.parents[1] / 'references' / 'example-deck.json'


def descendants(shapes):
    for shape in shapes:
        yield shape
        if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
            yield from descendants(shape.shapes)


class LayoutTests(unittest.TestCase):
    def test_layouts_fonts_notes_and_arrows(self):
        spec = json.loads(EXAMPLE.read_text())
        spec['slides'].append({
            'title': 'A clear capability and its team value', 'layout': 'cards',
            'cards': [
                {'label': 'CAPABILITY', 'lines': ['Useful tool discovery']},
                {'label': 'VALUE', 'lines': ['Simpler setup'], 'dark': True},
            ],
            'takeaway': 'Introduce value constructively.', 'notes': 'Generic test fixture.',
        })
        with TemporaryDirectory(prefix='management-slides-test-') as tmp:
            output = Path(tmp) / 'test.pptx'
            builder.build(spec, output)
            prs = Presentation(output)
            self.assertEqual(len(prs.slides), 7)
            self.assertEqual(prs.slide_width, builder.Inches(builder.WIDTH))
            for slide in prs.slides:
                self.assertTrue(slide.has_notes_slide)
                for shape in descendants(slide.shapes):
                    self.assertNotEqual(shape.shape_type, MSO_SHAPE_TYPE.PICTURE)
                    if not shape.has_text_frame:
                        continue
                    for para in shape.text_frame.paragraphs:
                        for run in para.runs:
                            self.assertEqual(run.font.name or para.font.name, 'Arial')
            # The first layout is a three-node flow with two directed connectors.
            arrows = prs.slides[0]._element.findall('.//' + qn('a:tailEnd'))
            self.assertEqual(len(arrows), 2)
            self.assertTrue(all(a.get('type') == 'triangle' for a in arrows))
            cards = [s for s in prs.slides[0].shapes if s.shape_type == MSO_SHAPE_TYPE.GROUP]
            self.assertEqual(len(cards), 3)
            self.assertTrue(all(len(s.shapes) == 4 for s in cards))
            self.assertTrue(all(any(p.name == 'card-heading' and p.has_text_frame
                                    for p in s.shapes) for s in cards))
            before = output.read_bytes()
            with self.assertRaises(FileExistsError):
                builder.build(spec, output)
            self.assertEqual(before, output.read_bytes())

    def test_system_layout_is_native_glued_and_guarded(self):
        spec = json.loads(EXAMPLE.read_text())
        spec['slides'] = [s for s in spec['slides'] if s.get('layout') == 'system']
        with TemporaryDirectory(prefix='management-slides-test-') as tmp:
            output = Path(tmp) / 'system.pptx'
            builder.build(spec, output)
            prs = Presentation(output)
            self.assertEqual(len(prs.slides), 2)
            for slide in prs.slides:
                shapes = list(descendants(slide.shapes))
                self.assertFalse([s for s in shapes if s.shape_type == MSO_SHAPE_TYPE.PICTURE])
                connectors = slide._element.findall('.//' + qn('p:cxnSp'))
                glued = [c for c in connectors if c.find('.//' + qn('a:stCxn')) is not None
                         or c.find('.//' + qn('a:endCxn')) is not None]
                self.assertGreater(len(glued), 0)
                for shape in shapes:
                    if shape.has_text_frame:
                        for para in shape.text_frame.paragraphs:
                            for run in para.runs:
                                self.assertEqual(run.font.name or para.font.name, 'Arial')
            first = prs.slides[0]
            self.assertTrue(first._element.findall('.//' + qn('a:prstDash')))
            names = {s.name for s in descendants(first.shapes)}
            self.assertTrue({'system-container', 'legend', 'alternate-return'} <= names)
            self.assertTrue(any(s.name.startswith('step-') for s in descendants(prs.slides[1].shapes)))

    def test_system_layout_rejects_overcrowded_or_unlinkable_input(self):
        base = {'title': 'T', 'takeaway': 'T', 'layout': 'system'}
        too_long = dict(base, columns=[
            {'nodes': [{'label': 'Overlong label ' * 12}]}
        ] + [{'nodes': [{'label': str(i)}]} for i in range(6)])
        unlinkable = dict(base, columns=[
            {'nodes': [{'label': 'A'}, {'label': 'B'}]},
            {'nodes': [{'label': 'C'}, {'label': 'D'}, {'label': 'E'}]}])
        for item in (too_long, unlinkable):
            with TemporaryDirectory(prefix='management-slides-test-') as tmp:
                with self.assertRaises(ValueError):
                    builder.build({'slides': [item]}, Path(tmp) / 'bad.pptx')

    def test_unknown_layout_rejected(self):
        with TemporaryDirectory(prefix='management-slides-test-') as tmp:
            with self.assertRaises(ValueError):
                builder.build({'slides': [{'title': 'Test', 'takeaway': 'Test',
                                          'layout': 'unknown'}]}, Path(tmp) / 'bad.pptx')


if __name__ == '__main__':
    unittest.main()
