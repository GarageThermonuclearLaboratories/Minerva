"""Regression checks for source integrity, repeatability and review preservation."""
import tempfile
import unittest
from pathlib import Path

from ingest_sources import ROOT, build, check, digest, encoded, read, register, save_json


class IngestionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        save_json(self.root / 'data/sources.json', {'snapshot_date': '2026-09-28', 'sources': []})
        save_json(self.root / 'data/ingestion-config.json', {'render_scale': 1.3, 'selected_pages': {}})
        self.input = ROOT / 'sources/originals/nys-math-standards-grade-7-crosswalk.pdf'
        self.record = self.root / 'record.json'
        save_json(self.record, {'id': 'src:test:crosswalk', 'title': 'Test registration of existing crosswalk',
                               'authority': 'NYSED', 'url': 'https://www.nysed.gov/',
                               'acquisition_method': 'test-fixture-copy', 'acquired_at': '2026-09-28',
                               'version': 'test only', 'role': 'supporting-draft-crosswalk'})

    def snapshot(self):
        return {str(p.relative_to(self.root)): digest(p.read_bytes())
                for p in self.root.rglob('*') if p.is_file()}

    def test_registration_and_repeatability_preserve_reviews(self):
        register(self.root, self.input, self.record)
        build(self.root)
        save_json(self.root / 'data/reviews/decision.json', {'status': 'review-in-progress'})
        before = self.snapshot()
        build(self.root)
        check(self.root)
        self.assertEqual(before, self.snapshot())
        receipt = read(self.root / 'data/ingestion-manifest.json')
        self.assertEqual(receipt['documents'][0]['page_count'], 13)
        self.assertFalse((self.root / 'data/ontology.json').exists())

    def test_changed_source_rejected_before_outputs(self):
        register(self.root, self.input, self.record)
        source = read(self.root / 'data/sources.json')['sources'][0]
        archive = self.root / source['archive_path']
        archive.write_bytes(archive.read_bytes() + b'changed')
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'integrity'):
            build(self.root)
        self.assertEqual(before, self.snapshot())

    def test_invalid_page_and_duplicate_id_do_not_mutate(self):
        register(self.root, self.input, self.record)
        save_json(self.root / 'data/ingestion-config.json',
                  {'render_scale': 1.3, 'selected_pages': {'src:test:crosswalk': [999]}})
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'Invalid evidence page'):
            build(self.root)
        with self.assertRaisesRegex(ValueError, 'already registered'):
            register(self.root, self.input, self.record)
        self.assertEqual(before, self.snapshot())

    def test_corrupt_output_is_detected_and_never_overwritten(self):
        register(self.root, self.input, self.record)
        receipt = build(self.root)
        artifact = self.root / receipt['documents'][0]['artifacts'][0]['path']
        artifact.write_bytes(b'corrupt')
        with self.assertRaisesRegex(ValueError, 'Artifact hash'):
            check(self.root)
        with self.assertRaisesRegex(ValueError, 'Generated output changed'):
            build(self.root)
        self.assertEqual(artifact.read_bytes(), b'corrupt')

    def test_error_page_cannot_be_archived_as_pdf(self):
        invalid = self.root / 'error.pdf'
        invalid.write_bytes(b'<html>502 Bad Gateway</html>')
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'not a PDF'):
            register(self.root, invalid, self.record)
        self.assertEqual(before, self.snapshot())

    def test_missing_evidence_artifact_cannot_evade_check(self):
        register(self.root, self.input, self.record)
        receipt = build(self.root)
        receipt['documents'][0]['artifacts'] = [a for a in receipt['documents'][0]['artifacts'] if not a['path'].endswith('.png')]
        save_json(self.root / 'data/ingestion-manifest.json', receipt)
        with self.assertRaisesRegex(ValueError, 'Artifact inventory'):
            check(self.root)

    def test_recipe_version_must_match(self):
        register(self.root, self.input, self.record)
        receipt = build(self.root)
        receipt['documents'][0]['recipe']['pymupdf'] = 'unknown'
        save_json(self.root / 'data/ingestion-manifest.json', receipt)
        with self.assertRaisesRegex(ValueError, 'stale'):
            check(self.root)


if __name__ == '__main__':
    unittest.main()
