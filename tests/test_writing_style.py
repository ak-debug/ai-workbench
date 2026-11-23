"""Package-contract checks, not an evaluation of model writing quality."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/personal-writing-style'
EXAMPLES = (
    'proposal.md',
    'team-message.md',
    'technical-feedback.md',
    'technical-blog-post.md',
    'linkedin-post.md',
)


class WritingStyleTests(unittest.TestCase):
    def test_complete_portable_bundle(self):
        for name in ('SKILL.md', 'README.md', 'global-instructions.md',
                     'references/writing-guide.md'):
            self.assertTrue((SKILL / name).is_file(), name)
        for name in EXAMPLES:
            self.assertTrue((SKILL / 'references/examples' / name).is_file(), name)

    def test_skill_routes_to_guide_and_examples(self):
        text = (SKILL / 'SKILL.md').read_text()
        self.assertIn('(references/writing-guide.md)', text)
        self.assertIn('(global-instructions.md)', text)
        for name in EXAMPLES:
            self.assertIn(f'(references/examples/{name})', text)

    def test_linkedin_guidance_covers_evidence_and_collaboration(self):
        guide = (SKILL / 'references/writing-guide.md').read_text()
        self.assertIn('## LinkedIn posts', guide)
        self.assertIn('credit collaborators', guide)
        self.assertIn('verified result', guide)
        self.assertIn('generic motivational slogan', guide)

    def test_copyable_global_baseline_is_short_and_names_skill(self):
        text = (SKILL / 'global-instructions.md').read_text()
        self.assertLess(len(text.split()), 300)
        self.assertIn('personal-writing-style', text)
        self.assertIn('handoff', text)
        self.assertIn('Do not invent', text)
        self.assertNotIn('---', text)

    def test_setup_requires_global_instructions_separately_from_skill(self):
        readme = (SKILL / 'README.md').read_text()
        self.assertIn('## Step 1: install the complete skill folder', readme)
        self.assertIn('## Step 2: merge the global writing instructions', readme)
        self.assertIn('(global-instructions.md)', readme)
        self.assertIn('not the global instructions', readme)
        root_readme = (ROOT / 'README.md').read_text()
        self.assertIn('two setup steps', root_readme)
        self.assertIn('(skills/personal-writing-style/global-instructions.md)', root_readme)

    def test_package_local_links_survive_standalone_copy(self):
        for path in SKILL.rglob('*.md'):
            with self.subTest(path=path.relative_to(SKILL)):
                text = path.read_text()
                for target in re.findall(r'!?\[[^\]]*\]\(([^\s)]+)\)', text):
                    if '://' in target or target.startswith(('#', 'mailto:')):
                        continue
                    resolved = (path.parent / target.split('#')[0]).resolve()
                    self.assertTrue(resolved.is_relative_to(SKILL.resolve()), target)
                    self.assertTrue(resolved.exists(), target)

    def test_instruction_only_package_has_no_execution_or_hook_metadata(self):
        for path in SKILL.rglob('*'):
            if path.is_file():
                self.assertEqual(path.suffix, '.md', path.name)
        text = (SKILL / 'SKILL.md').read_text()
        frontmatter = text.split('---', 2)[1]
        for key in ('hooks:', 'allowed-tools:', 'context:', 'model:'):
            self.assertNotIn(key, frontmatter)
        self.assertNotIn('!`', text)

    def test_examples_are_labelled_fictional(self):
        for name in EXAMPLES:
            text = (SKILL / 'references/examples' / name).read_text()
            self.assertIn('Fictional example.', text)
            self.assertIn('\n---\n', text)

    def test_catalog_selects_only_the_new_skill(self):
        catalog = json.loads((ROOT / '.claude-plugin/marketplace.json').read_text())
        entries = {item['name']: item for item in catalog['plugins']}
        self.assertEqual(entries['personal-writing-style']['skills'],
                         ['./skills/personal-writing-style'])
        self.assertEqual(entries['personal-writing-style']['source'], './')
        self.assertFalse(entries['personal-writing-style']['strict'])
        self.assertEqual(entries['management-slides']['version'], '1.1.0')
        self.assertEqual(entries['personal-writing-style']['version'], '1.5.0')


if __name__ == '__main__':
    unittest.main()
