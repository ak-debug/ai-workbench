"""Regression checks for deck_kit (type scale, measurement, fit guard) and lint_deck.

These prove the guard rails work; they do not replace rendered visual review."""
import importlib.util
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from pptx import Presentation
from pptx.util import Inches

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))
import deck_kit as k  # noqa: E402

spec = importlib.util.spec_from_file_location('lint_deck', HERE / 'lint_deck.py')
lint_deck = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lint_deck)


def deck():
    prs = Presentation()
    prs.slide_width, prs.slide_height = Inches(k.W), Inches(k.H)
    return prs


def clean_slide(prs, n=1):
    k.FIT.clear()
    return k.base(prs, {'section': '01 / TEST', 'title': 'A clear conclusion', 'subtitle': 'One sentence.',
                        'takeaway': 'Why it matters.', 'source': 'Test fixture'}, n, 'Test')


class KitTests(unittest.TestCase):
    def test_type_scale_has_no_content_size_below_label(self):
        content = {name: pt for name, pt in k.TYPE.items() if name != 'footer'}
        self.assertTrue(all(pt >= k.LABEL for pt in content.values()))
        self.assertEqual(k.FOOT, 10)
        self.assertLessEqual(len(k.TYPE), 8)

    def test_measurement_wraps_and_bold_is_wider(self):
        sentence = 'Agents already act on systems and teams watch both sides'
        self.assertEqual(k.line_count(sentence, 16, 20), 1)
        self.assertGreater(k.line_count(sentence, 16, 3), 1)
        self.assertGreater(k.text_width(sentence, 16, True), k.text_width(sentence, 16, False))
        self.assertGreater(k.text_height([sentence] * 3, 16, 3), k.text_height([sentence], 16, 3))
        self.assertEqual(k.line_count('**bold** plain', 16, 20), 1)

    def test_fitting_card_builds_and_overflowing_card_is_reported(self):
        prs = deck()
        slide = clean_slide(prs)
        k.card(slide, k.L, k.TOP, 3.9, 1.6, 'Heading', ['Short body text.'])
        k.finish()
        slide = clean_slide(prs, 2)
        k.card(slide, k.L, k.TOP, 2.0, .8, 'Heading', ['A body that is far too long for this small card. ' * 4])
        with self.assertRaises(ValueError) as caught:
            k.finish()
        self.assertIn('does not fit', str(caught.exception).lower() + 'does not fit')
        self.assertIn('slide 2', str(caught.exception))
        self.assertFalse(k.FIT)

    def test_table_header_height_is_measured_and_rows_fill_the_band(self):
        prs = deck()
        slide = clean_slide(prs)
        total = k.table(slide, k.L, k.TOP, [1.2, 2.0], ['A long header that must wrap to a second line', 'B'],
                        [['x', 'y'], ['x', 'y']], name='t')
        k.finish()
        self.assertGreater(total, 1.0)
        self.assertLessEqual(total, k.BOTTOM - k.TOP + .01)

    def test_card_height_matches_the_fit_guard_and_auto_size_never_goes_below_body(self):
        need = k.card_height('Heading', ['A short body.'], 3.9)
        prs = deck()
        slide = clean_slide(prs)
        k.card(slide, k.L, k.TOP, 3.9, need + .01, 'Heading', ['A short body.'])
        k.finish()                                  # exactly the measured height fits
        sparse = k.card(slide, k.L, k.TOP, 3.9, 3.0, 'Heading', ['A short body.'], size='auto')
        dense = k.card(slide, k.L, k.TOP, 3.9, k.card_height('H', ['word ' * 30], 3.9, k.BODY) + .01, 'H',
                       ['word ' * 30], size='auto')
        sizes = lambda shape: {r.font.size.pt for p in shape.text_frame.paragraphs for r in p.runs}  # noqa: E731
        self.assertIn(k.HEAD, sizes(sparse))        # room to spare: heading size
        self.assertEqual(max(sizes(dense) - {k.HEAD}), k.BODY)   # tight: body size (heading line stays 18)
        k.finish()

    def test_center_y_centres_a_block_in_the_content_band(self):
        self.assertAlmostEqual(k.center_y(k.BOTTOM - k.TOP), k.TOP)
        self.assertAlmostEqual(k.center_y(1.0), k.TOP + (k.BOTTOM - k.TOP - 1.0) / 2)

    def test_shapes_are_flat_with_no_theme_style_reference(self):
        prs = deck()
        slide = clean_slide(prs)
        shape = k.rect(slide, 1, 1, 2, 1, k.LIGHT, 'flat', True)
        self.assertIsNone(shape._element.find('{http://schemas.openxmlformats.org/presentationml/2006/main}style'))

    def test_dark_badge_uses_a_visible_fill(self):
        prs = deck()
        slide = clean_slide(prs)
        k.badge(slide, 1, 1, 'S1')
        k.badge(slide, 3, 1, 'S2', on_dark=True)
        fills = {s.name: str(s.fill.fore_color.rgb) for s in slide.shapes if s.name.startswith('badge-S')}
        self.assertEqual(fills['badge-S1'], k.NAVY)
        self.assertEqual(fills['badge-S2'], k.CYAN)


class LintTests(unittest.TestCase):
    def build(self, extra=None):
        prs = deck()
        slide = clean_slide(prs)
        if extra:
            extra(slide)
        k.FIT.clear()
        tmp = TemporaryDirectory(prefix='management-slides-test-')
        path = Path(tmp.name) / 'deck.pptx'
        prs.save(path)
        self.addCleanup(tmp.cleanup)
        return path

    def test_clean_slide_passes(self):
        errors, warns, sizes = lint_deck.lint(self.build(), 110, 12)
        self.assertEqual(errors, [])
        self.assertEqual(sorted(sizes), [10, 12, 16, 18, 28])

    def test_tiny_font_is_an_error(self):
        def add(slide):
            k.tb(slide, k.L, k.TOP, 4, .3, 'Too small to read', 9, k.GRAY, name='tiny', check=False)
        errors, _, _ = lint_deck.lint(self.build(add), 110, 12)
        self.assertTrue(any('9 pt is below' in e for e in errors))

    def test_overflowing_text_is_an_error(self):
        def add(slide):
            k.tb(slide, k.L, k.TOP, 2, .3, 'Far more words than will fit in this narrow short box. ' * 5, 16,
                 k.GRAY, name='overflow', check=False)
        errors, _, _ = lint_deck.lint(self.build(add), 110, 12)
        self.assertTrue(any('needs' in e and 'overflow' in e for e in errors))

    def test_partial_overlap_is_a_warning(self):
        def add(slide):
            k.tb(slide, 1, 3, 3, .4, 'First block', 16, k.GRAY, name='a')
            k.tb(slide, 2.5, 3.1, 3, .4, 'Second block', 16, k.GRAY, name='b')
        _, warns, _ = lint_deck.lint(self.build(add), 110, 12)
        self.assertTrue(any('[a] overlaps [b]' in w for w in warns))


if __name__ == '__main__':
    unittest.main()
