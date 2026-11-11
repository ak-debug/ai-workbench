"""Preview generation safety tests; do not need fonts or a presentation renderer."""
import importlib.util
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location(
    'preview', ROOT / 'skills/management-slides/scripts/build_preview.py')
preview = importlib.util.module_from_spec(loader)
loader.loader.exec_module(preview)


class PreviewTests(unittest.TestCase):
    def test_existing_preview_is_not_overwritten(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / 'preview.png'
            output.write_bytes(b'original')
            with self.assertRaises(FileExistsError):
                preview.build(output, 'unused-font.ttf', 'unused-bold.ttf')
            self.assertEqual(output.read_bytes(), b'original')

    def test_non_png_output_is_rejected(self):
        with TemporaryDirectory() as directory:
            output = Path(directory) / 'preview.jpg'
            with self.assertRaises(ValueError):
                preview.build(output, 'unused-font.ttf', 'unused-bold.ttf')
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
