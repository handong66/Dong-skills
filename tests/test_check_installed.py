import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check-installed.py'


class CheckInstalled(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / 'source'
        self.installed = self.root / 'installed'
        self.skill = self.source / 'example'
        (self.skill / 'references').mkdir(parents=True)
        (self.skill / 'SKILL.md').write_text('source entry\n')
        (self.skill / 'references/evidence.md').write_text('source evidence\n')
        shutil.copytree(self.source, self.installed)

    def run_check(self, *extra):
        return subprocess.run([sys.executable, str(SCRIPT), '--source', str(self.source),
                               '--installed', str(self.installed), *extra], capture_output=True, text=True)

    def rows(self, result):
        return {row['path']: row for row in json.loads(result.stdout)['skills'][0]['entries']}

    def test_exact_match_and_independent_hash(self):
        result = self.run_check()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.rows(result)['SKILL.md']['source']['sha256'], hashlib.sha256(b'source entry\n').hexdigest())

    def test_stale_missing_extra_and_empty_directory_without_mutation(self):
        dest = self.installed / 'example'
        (dest / 'SKILL.md').write_text('local edit\n')
        (dest / 'references/evidence.md').unlink()
        (dest / 'extra.txt').write_text('keep me\n')
        (dest / 'empty').mkdir()
        before = {str(p): (p.read_bytes() if p.is_file() else None) for p in self.root.rglob('*')}
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        rows = self.rows(result)
        for path, status in [('SKILL.md', 'stale'), ('references/evidence.md', 'missing'), ('extra.txt', 'extra'), ('empty', 'extra')]:
            self.assertEqual(rows[path]['status'], status)
        after = {str(p): (p.read_bytes() if p.is_file() else None) for p in self.root.rglob('*')}
        self.assertEqual(before, after)

    def test_missing_installation_does_not_create_it(self):
        shutil.rmtree(self.installed)
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        self.assertFalse(self.installed.exists())
        self.assertTrue(all(row['status'] == 'missing' for row in self.rows(result).values()))

    def test_symlink_file_and_directory_are_not_traversed(self):
        dest = self.installed / 'example'
        external = self.root / 'outside'
        external.mkdir()
        (external / 'private.txt').write_text('DO_NOT_READ_THIS')
        (dest / 'link').symlink_to(external, target_is_directory=True)
        (dest / 'dangling').symlink_to(self.root / 'absent')
        result = self.run_check()
        self.assertEqual(result.returncode, 1)
        rows = self.rows(result)
        self.assertEqual(rows['link']['status'], 'unsupported')
        self.assertEqual(rows['dangling']['status'], 'unsupported')
        self.assertNotIn('link/private.txt', rows)
        self.assertNotIn('DO_NOT_READ_THIS', result.stdout)

    def test_symlink_installation_and_root_are_refused(self):
        dest = self.installed / 'example'
        shutil.rmtree(dest)
        dest.symlink_to(self.skill, target_is_directory=True)
        self.assertEqual(self.rows(self.run_check())['.']['status'], 'unsupported')
        alias = self.root / 'alias'
        alias.symlink_to(self.installed, target_is_directory=True)
        self.assertEqual(self.run_check('--installed', str(alias)).returncode, 2)

    def test_invalid_source_or_traversal_fails(self):
        for name in ('../outside', '.', 'absent'):
            with self.subTest(name=name):
                self.assertEqual(self.run_check('--skill', name).returncode, 2)
        (self.skill / 'SKILL.md').unlink()
        self.assertEqual(self.run_check().returncode, 2)

    def test_other_installed_skills_are_outside_selection(self):
        (self.installed / 'unrelated').mkdir()
        self.assertEqual(self.run_check('--skill', 'example').returncode, 0)


if __name__ == '__main__':
    unittest.main()
