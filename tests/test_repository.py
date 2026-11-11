"""Tests for catalog containment and publication guardrails; no live credentials."""
import importlib.util
import struct
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

ROOT = Path(__file__).resolve().parents[1]
loader = importlib.util.spec_from_file_location('validator', ROOT / 'scripts/validate_repo.py')
validator = importlib.util.module_from_spec(loader)
loader.loader.exec_module(validator)


class RepositoryTests(unittest.TestCase):
    def test_repository_validates(self):
        self.assertEqual(validator.validate(ROOT), [])

    def test_synthetic_token_is_detected_without_echoing(self):
        sample = 'gh' + 'p_' + 'x' * 36
        self.assertIn('credential-like token', validator.scan_text(sample))
        self.assertNotIn(sample, str(validator.scan_text(sample)))

    def test_synthetic_personal_path_is_detected(self):
        sample = '/' + 'Users' + '/example-person/private/'
        self.assertIn('personal absolute path', validator.scan_text(sample))

    def test_extra_private_identifier_is_detected(self):
        self.assertEqual(validator.scan_text('example phrase', ['EXAMPLE PHRASE']),
                         ['explicitly disallowed text'])

    def test_placeholder_urls_are_allowed(self):
        self.assertEqual(validator.scan_text('https://github.com/example-owner/example-repo'), [])

    def test_parent_traversal_is_rejected(self):
        with TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                validator.local_path(Path(directory), './../outside')

    def test_absolute_catalog_path_is_rejected(self):
        with TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                validator.local_path(Path(directory), directory)

    def test_missing_catalog_directory_is_rejected(self):
        with TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                validator.local_path(Path(directory), './missing')

    def test_preview_has_only_pixel_chunks(self):
        data = (ROOT / 'skills/management-slides/assets/style-preview.png').read_bytes()
        self.assertEqual(set(validator.png_chunks(data)), {b'IHDR', b'IDAT', b'IEND'})
        self.assertEqual(struct.unpack('>II', data[16:24]), (1800, 1100))

    def test_truncated_png_is_rejected(self):
        with self.assertRaises(ValueError):
            validator.png_chunks(b'\x89PNG\r\n\x1a\n' + b'broken')


if __name__ == '__main__':
    unittest.main()
