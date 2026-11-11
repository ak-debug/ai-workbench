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
            self.assertEqual(len(prs.slides), 5)
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

    def test_unknown_layout_rejected(self):
        with TemporaryDirectory(prefix='management-slides-test-') as tmp:
            with self.assertRaises(ValueError):
                builder.build({'slides': [{'title': 'Test', 'takeaway': 'Test',
                                          'layout': 'unknown'}]}, Path(tmp) / 'bad.pptx')


if __name__ == '__main__':
    unittest.main()
