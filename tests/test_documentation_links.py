"""Synthetic Markdown fixtures; no private saves or game-directory access."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location('doc_links', Path(__file__).resolve().parents[1] / 'tools/check_documentation_links.py')
LINKS = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINKS)


class DocumentationLinksTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def write(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')

    def test_relative_links_and_unicode_anchor(self):
        self.write('README.md', '[guide](docs/guide.md#evidence-æther)')
        self.write('docs/guide.md', '# Evidence `Æther`\n[home](../README.md)')
        result = LINKS.check(self.root)
        self.assertEqual([], result['errors'])
        self.assertEqual(2, result['local_links_checked'])

    def test_missing_target_and_anchor(self):
        self.write('README.md', '[bad](absent.md) [anchor](#wrong)\n# Real')
        self.assertEqual(2, len(LINKS.check(self.root)['errors']))

    def test_fenced_and_inline_examples_ignored(self):
        self.write('README.md', '```md\n[x](absent.md)\n```\n`[y](missing.md)`')
        self.assertEqual([], LINKS.check(self.root)['errors'])

    def test_explicit_doc_reference_is_checked(self):
        self.write('README.md', '`docs/absent.md`')
        self.assertEqual(1, len(LINKS.check(self.root)['errors']))

    def test_private_backup_and_dependency_files_excluded(self):
        for folder in ('data/raw/player_save', 'backups', 'artifacts', 'photograph/.venv'):
            self.write(folder + '/private.md', '[broken](absent.md)')
        self.write('README.md', '# Public')
        result = LINKS.check(self.root)
        self.assertEqual(1, result['markdown_files'])
        self.assertEqual([], result['errors'])

    def test_duplicate_heading_anchor(self):
        self.write('README.md', '# Same\n# Same\n[second](#same-1)')
        self.assertEqual([], LINKS.check(self.root)['errors'])

    def test_reference_link_spaces_and_images(self):
        self.write('README.md', '[doc][ref]\n[ref]: <docs/a b.md>\n![diagram](diagram.png)')
        self.write('docs/a b.md', '# A')
        self.write('diagram.png', 'fixture')
        self.assertEqual([], LINKS.check(self.root)['errors'])

    def test_external_not_fetched_and_escape_rejected(self):
        self.write('README.md', '[web](https://example.invalid/a#x) [escape](../outside.md)')
        result = LINKS.check(self.root)
        self.assertEqual(1, result['external_links_not_fetched'])
        self.assertEqual(1, len(result['errors']))


if __name__ == '__main__':
    unittest.main()
